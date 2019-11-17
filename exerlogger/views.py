from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

# Create your views here.
from exerlogger.forms import NewWorkoutForm
from .models import Drill, Exercise, Workout


@login_required
def user_homepage(request, self=None):
    context = {}

    # drills
    all_drills = Drill.objects.all()
    context.update({'all_drills': all_drills})

    # exercises
    all_exercises = Exercise.objects.all()
    context.update({'all_exercises': all_exercises})

    # workouts only for user
    user_workouts = Workout.objects.filter(user=request.user).order_by('-id')
    context.update({'user_workouts': user_workouts})

    return render(request, 'userspace/index.html', context)


@login_required
def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    return render(request, 'workout/detail.html', {'workout': workout})


@login_required
def new_workout(request):
    # form to input a new workout
    workout_form = NewWorkoutForm(request.POST or None)

    if workout_form.is_valid():
        instance = workout_form.save(commit=False)
        # will save workout under currently logged user
        instance.user = request.user
        # save data to db
        instance.save()
        return redirect('home')

    context = {
        "workout_form": workout_form
    }

    return render(request, "workout/new.html", context)


