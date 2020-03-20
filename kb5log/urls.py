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
from exerlogger.views import user_homepage, signup_view

app_name = 'exerlogger'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup_view, name="signup"),

    # User homepage
    path('', user_homepage, name='home'),
    # List of workouts
    path('workouts/', views.workouts, name='workouts'),
    # New Workout
    url(r'workouts/(add)/', views.workout_detail, name='workout_new'),
    # List of exercises for single workout
    path('workouts/<workout_id>/', views.workout_detail, name='workout_detail'),
    # Edit single exercise in single workout
    path('workouts/<int:workout_id>/<int:exercise_id>/', views.workout_detail, name='exercise_edit'),
    # Delete exercise
    path('workouts/<int:workout_id>/<int:exercise_id>/delete', views.delete_item, name='delete_exercise'),
    # Delete Workout
    path('workouts/<int:workout_id>/delete', views.delete_item, name='delete_workout'),
    # Email change
    path('change_profile', views.user_profile_change, name='user_profile_change'),
    # User attendance
    path('attendance', views.attendance, name='attendance'),
    # Calendar view
    path('calendar', views.calendar_view, name='calendar')
]