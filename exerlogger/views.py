from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

# Create your views here.
from exerlogger.forms import NewWorkoutForm, NewExerciseForm
from .models import Drill, Exercise, Workout
from django.forms import modelformset_factory


@login_required
def user_homepage(request, self=None):
    context = {}

    return render(request, 'userspace/index.html', context)


@login_required
def workouts(request):
    # workouts only for user
    user_workouts = Workout.objects.filter(user=request.user).order_by('-id')
    context = {'user_workouts': user_workouts}

    return render(request, 'workout/workouts.html', context)


@login_required
def workout_detail(request):
    workout = get_object_or_404(Workout, pk=workout_id)
    exercises = Exercise.objects.filter(workout=workout_id)

    context = {
        'workout': workout,
        'exercises': exercises
    }
    # list of workouts /workouts/
    if request.method == 'GET':
        orkout = get_object_or_404(Workout, pk=workout_id)
        exercises = Exercise.objects.filter(workout=workout_id)
        }
    if request.method == 'POST':
        exercise_form = NewExerciseForm(request.POST or None)
        if "add" in request.path_info:
            # new workout object
            workout_current = Workout.objects.create()
            context = {
                'workout_current': workout_current,
                'form': exercise_form
            }

    return render(request, 'workout/workout_detail.html', context)


@login_required
def new_workout(request): #TODO OBSOLETE
    # form to input a new workout
    # workout_form = NewWorkoutForm(request.POST or None)

    # if workout_form.is_valid():
    #     instance = workout_form.save(commit=False)
    #     # will save workout under currently logged user
    #     instance.user = request.user
    #     # save data to db
    #     instance.save()
    # return

    #TODO ideal je mit pri otevreni stranky s new ulozen new workout a mit id workoutu k dispozici
    #TODO s workout ID pracovat pri ukladani formulare pro exercise


    #vytvori workout object v db po kazdem zobrazeni new_worjout stranky > TODO vytvori po kazdem refresh to je CHYBA
    workout_current = Workout.objects.create()

    #pokud je Post vytvori form
    exercise_form = NewExerciseForm(request.POST.copy() or None)

    #pokud je form validni
    if exercise_form.is_valid():
        #exercise_form = exercise_form.copy()
        #mel by pridat workout id k datum z formulare > TODO nefunguje > This QueryDict instance is immutable

        exercise_form.data['Workout'] = workout_current.id
        #vytvori instanci a jeste neulozi
        exercise_instance = exercise_form.save(commit=False)
        #ulozi do db
        exercise_instance.save()

    # exercises
    current_workout_exercises = Exercise.objects.filter(workout=workout_current)

    context = {
        "exercise_form": exercise_form,
        "current_workout": workout_current,
        "current_workout_exercises": current_workout_exercises
    }

    return render(request, "workout/new.html", context)



