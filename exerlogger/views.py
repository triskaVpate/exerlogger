from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from exerlogger.forms import NewExerciseForm, CustomUserCreationForm
from .models import Exercise, Workout


@login_required
def user_homepage(request):
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
        exercise_form = NewExerciseForm(request.POST)
        # when POST is initialized for the first time, create workout and use it for form
        if request.method == "POST":
            workout_current = Workout.objects.create()
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
            request.POST,
            instance=Exercise(workout=workout)
        )
        if exercise_form.is_valid():
            exercise_form.save(commit=True)

        context = {
            'workout': workout,
            'exercises': exercises,
            'exercise_form': exercise_form
        }

    return render(request, 'workout/workout_detail.html', context)
