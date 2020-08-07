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
    # Drill - Program
    ## Add - Drill
    # path('programs/<int:program_id>/drills/add', , name='drill_add'), # ADD View
    ## Remove - Drill
    # path('programs/<int:program_id>/drills/<id_drill>/remove', ,name='drill_remove') # ADD View
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
    # Performance - Workout
    ## New - Performance
    path('workout/<int:workout_id>/Performances/new/', views.PerformanceCreateView.as_view(), name='performance_new'),
    ## Detail - Performance
    path('workout/<int:workout_id>/Performances/<int:performance_id>', views.PerformanceDetailView.as_view(), name='performance_detail'),
    ## Edit - Performance
    path('workout/<int:workout_id>/Performances/<int:performance_id>/edit', views.PerformanceUpdateView.as_view(), name='performance_edit'),
    ## Delete - Performance
    path('workout/<int:workout_id>/Performances/<int:performance_id>/delete', views.PerformanceDeleteView.as_view(), name='performance_delete'),
    # Email change
    path('change_profile', views.user_profile_change, name='user_profile_change'),
    # User attendance
    path('attendance', views.attendance, name='attendance'),
    # User attendance
    path('payments', views.payments, name='payments')
]
