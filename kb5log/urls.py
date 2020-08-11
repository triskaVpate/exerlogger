"""kb5log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from exerlogger import views

app_name = 'exerlogger'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup_view, name="signup"),

    # User homepage
    path('', views.user_homepage, name='home'),
    # Program
    ## List - Program
    path('programs/',views.ProgramListView.as_view(), name='program_list'),
    ## New - Program
    path('programs/new/',views.ProgramCreateView.as_view(), name='program_new'),
    ## Detail - Program
    path('programs/<int:program_id>/', views.ProgramDetailView.as_view(), name='program_detail'),
    ## Edit - Program
    path('programs/<int:program_id>/edit', views.ProgramUpdateView.as_view(), name='program_edit'),
    ## Delete - Program
    path('programs/<int:program_id>/delete', views.ProgramDeleteView.as_view(), name='program_delete'),
    # Drill
    ## List - Drill
    path('drills/', views.DrillListView.as_view(), name='drill_list'),
    ## New - Drill
    path('drills/new/', views.DrillCreateView.as_view(), name='drill_new'),
    ## Detail - Drill
    path('drills/<int:drill_id>', views.DrillDetailView.as_view(), name='drill_detail'),
    ## Edit - Drill
    path('drills/<int:drill_id>/edit', views.DrillUpdateView.as_view(), name='drill_edit'),
    ## Delete - Drill
    path('drills/<int:drill_id>/delete', views.DrillDeleteView.as_view(), name='drill_delete'),
    # Workout
    ## List - Workout
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    ## New - Workout
    path('workouts/new/', views.WorkoutCreateView.as_view(), name='workout_new'),
    ## Detail - Workout
    path('workouts/<int:workout_id>', views.WorkoutDetailView.as_view(), name='workout_detail'),
    ## Edit - Workout
    path('workouts/<int:workout_id>/edit', views.WorkoutUpdateView.as_view(), name='workout_edit'),
    ## Delete - Workout
    path('workouts/<int:workout_id>/delete', views.WorkoutDeleteView.as_view(), name='workout_delete'),
    # Exercise - Workout
    ## List - Exercise
    path('workouts/<int:workout_id>/exercises/', views.ExerciseListView.as_view(), name='exercise_list'),
    ## New - Exercise
    path('workouts/<int:workout_id>/exercises/new/', views.ExerciseCreateView.as_view(), name='exercise_new'),
    ## Detail - Exercise
    path('workouts/<int:workout_id>/exercises/<int:exercise_id>', views.ExerciseDetailView.as_view(), name='exercise_detail'),
    ## Edit - Exercise
    path('workouts/<int:workout_id>/exercises/<int:exercise_id>/edit', views.ExerciseUpdateView.as_view(), name='exercise_edit'),
    ## Delete - Exercise
    path('workouts/<int:workout_id>/exercises/<int:exercise_id>/delete', views.ExerciseDeleteView.as_view(), name='exercise_delete'),
    # Performance - Exercise
    ## New - Performance
    path('workouts/<int:workout_id>/exercises/<int:exercise_id>/performances/new/', views.PerformanceCreateView.as_view(), name='performance_new'),
    ## Detail - Performance
    path('exercises/<int:exercise_id>/performances/<int:performance_id>', views.PerformanceDetailView.as_view(), name='performance_detail'),
    ## Edit - Performance
    path('exercises/<int:exercise_id>/performances/<int:performance_id>/edit', views.PerformanceUpdateView.as_view(), name='performance_edit'),
    ## Delete - Performance
    path('exercises/<int:exercise_id>/performances/<int:performance_id>/delete', views.PerformanceDeleteView.as_view(), name='performance_delete'),
    # Email change
    path('change_profile', views.user_profile_change, name='user_profile_change'),
    # User attendance
    path('attendance', views.attendance, name='attendance'),
    # User attendance
    path('payments', views.payments, name='payments')
]
