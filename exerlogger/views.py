from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.safestring import mark_safe

from exerlogger.forms import NewExerciseForm, CustomUserCreationForm, CustomUserChangeForm, CustomUserEmailChangeForm, \
    CustomUserAdvancedChangeForm
from .models import Exercise, Workout, CustomUser, Training, Payment
from .utils import Calendar
from calendar import HTMLCalendar
# from datetime import datetime
import datetime


@login_required
def payments(request):
    user_payments = Payment.objects.filter(var_num=request.user.var_num).order_by('-date')
    context = {'user_payments': user_payments}
    return render(request, 'payments/payments.html', context)


@login_required
def calendar_view(request):
    context = {}
    # Instantiate our calendar class with today's year and date

    d = datetime.date.today()
    cal = HTMLCalendar()

    # Call the formatmonth method, which returns our calendar as a table
    html_cal = cal.formatmonth(d.year, d.month, withyear=True)
    context['calendar'] = mark_safe(html_cal)
    return render(request, 'calendar/calendar.html', context)


@login_required
def attendance(request):
    user_trainings = request.user.training_set.all()
    list_user_trainings = []
    for training in user_trainings:
        list_user_trainings.append(training.id)
    all_trainings = Training.objects.filter(lesson=request.user.lesson).order_by('-date')
    context = {'user_trainings': user_trainings, 'list_user_trainings': list_user_trainings,
               'all_trainings': all_trainings}
    return render(request, 'attendance/attendance.html', context)


@login_required
def user_profile_change(request):
    user = get_object_or_404(CustomUser, username=request.user)
    # form = CustomUserEmailChangeForm(request.POST or None, instance=user)
    form = CustomUserAdvancedChangeForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save(commit=True)
        return redirect(user_profile_change)

    context = {'form': form, 'user': user}
    return render(request, 'registration/profile_change_form.html', context)


@login_required
def user_homepage(request):
    # which lesson is user member of
    # user_lesson =

    context = {}

    return render(request, 'userspace/index.html', context)


def signup_view(request):
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html', {'form': form})


@login_required
def workouts(request):
    # workouts only for user
    user_workouts = Workout.objects.filter(user=request.user).order_by('-id')
    context = {'user_workouts': user_workouts}
    return render(request, 'workout/workouts.html', context)


@login_required
def delete_item(request, workout_id=None, exercise_id=None):
    if request.method == 'POST':
        if exercise_id:
            get_object_or_404(Exercise, id=exercise_id).delete()
            return redirect(workout_detail, workout_id=workout_id)
        else:
            get_object_or_404(Workout, id=workout_id).delete()
            return redirect(workouts)


@login_required
def workout_detail(request, workout_id, exercise_id=None):
    # New workout branch
    if workout_id == "add":
        # show empty form
        submitted = False
        exercise_form = NewExerciseForm()
        # when POST is initialized for the first time, create workout and use it for form
        if request.method == 'POST':
            workout_current = Workout.objects.create(user=request.user)
            exercise_form = NewExerciseForm(request.POST)
            exercise_form.instance = Exercise(workout=workout_current)
            if exercise_form.is_valid():
                exercise_form.save(commit=True)
                # when first exercise is saved, redirect to the other branch of this view
                return redirect(workout_detail, workout_id=workout_current.id)
        context = {
            'exercise_form': exercise_form
        }

    # editing exercise - load exercise parameter in form
    elif exercise_id is not None:
        workout = get_object_or_404(Workout, pk=workout_id)
        exercises = Exercise.objects.filter(workout=workout_id)
        exercise_item = get_object_or_404(Exercise, id=exercise_id)
        exercise_form = NewExerciseForm(request.POST or None, instance=exercise_item)

        if exercise_form.is_valid():
            exercise_form.save()
            # once form is saved, redirect on the same page to have clear form ready
            return redirect(workout_detail, workout_id=workout.id)
        context = {
            'workout': workout,
            'exercises': exercises,
            'exercise_form': exercise_form
        }
    # workout details?
    else:
        workout = get_object_or_404(Workout, pk=workout_id)
        exercises = Exercise.objects.filter(workout=workout_id)

        exercise_form = NewExerciseForm(
            request.POST or None,
            instance=Exercise(workout=workout)
        )
        if exercise_form.is_valid():
            exercise_form.save(commit=True)
            # once form is saved, redirect on the same page to have clear form ready
            return redirect(workout_detail, workout_id=workout.id)

        context = {
            'workout': workout,
            'exercises': exercises,
            'exercise_form': exercise_form
        }

    return render(request, 'workout/workout_detail.html', context)
