from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.safestring import mark_safe

from exerlogger.forms import (NewExerciseForm, CustomUserCreationForm,
                              CustomUserAdvancedChangeForm, DrillForm,
                              ExerciseForm, WorkoutForm, PerformanceForm)
from .models import (Exercise, Workout, CustomUser,
                     Training, Payment, Program,
                     Performance)
from .utils import Calendar
# from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
# Class Based Views imports
from django.views.generic import (TmeplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


@login_required
def payments(request):
    user_payments = Payment.objects.filter(var_num=request.user.var_num).order_by('-date')
    user_membership = request.user.membership

    if type(user_membership) is dict:
        user_membership = user_membership['2020']

    months_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    context = {'user_payments': user_payments, 'months_list': months_list, 'user_membership': user_membership}
    return render(request, 'payments/payments.html', context)


@login_required
def attendance(request):
    # list of training sessions for loging that user is present or missing
    user_trainings = request.user.training_set.all()
    list_user_trainings = []
    for training in user_trainings:
        list_user_trainings.append(training.id)
    all_trainings = Training.objects.filter(lesson=request.user.lesson).order_by('-date')
    context = {'user_trainings': user_trainings, 'list_user_trainings': list_user_trainings,
               'all_trainings': all_trainings}

    # calendar part
    d = datetime.date.today()

    # calendar movement start
    move = request.GET.get('move', None)
    month_id = request.GET.get('month_id', None)
    year_id = request.GET.get('year_id', None)

    if month_id is not None and move == "previous_month":
        d = d.replace(month=int(month_id))+relativedelta(months=-1, year=int(year_id))
    elif month_id is not None and move == "next_month":
        d = d.replace(month=int(month_id))+relativedelta(months=+1, year=int(year_id))
    # calendar movement end

    cal = Calendar(d.year, d.month)

    # Call the formatmonth method, which returns our calendar as a table
    html_cal = cal.formatmonth(withyear=True, username=request.user)
    context['calendar'] = mark_safe(html_cal)
    # this exist cause of moving to different months
    context['month_id'] = d.month
    context['year_id'] = d.year

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
    # show empty form
    form = CustomUserCreationForm()
    # if post, do the thing
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # after save lets authenticate user, login him and redirect to homepage
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


# Program
class ProgramListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Program

class ProgramCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Program
    redirect_field_name = # ADD
    form_class = ProgramForm


class ProgramDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Program


class ProgramUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Program
    redirect_field_name = # ADD
    form_class = ProogramForm


class ProgramDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


# Workout
class WorkoutListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Workout


class WorkoutDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Workout


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Workout
    redirect_field_name = # ADD
    form_class = WorkoutForm


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Workout
    redirect_field_name = # ADD
    form_class =WorkoutForm


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Workout
    success_url = # ADD


# Performance
class PerformanceCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Performance
    redirect_field_name = # ADD
    form_class = PerformanceForm


class PerformanceDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Performance


class PerformanceUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Performance
    redirect_field_name = # ADD
    form_class = PerformanceForm


class PerformanceDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Performance
    success_url = reverse_lazy() # ADD
