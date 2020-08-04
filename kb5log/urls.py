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
from exerlogger.views # import user_homepage, signup_view

app_name = 'exerlogger'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup_view, name="signup"),

    # User homepage
    path('', user_homepage, name='home'),
    # Program
    path('programs/',views.ProgramListView.as_view(), name='program_list'),
    path('programs/new/',views.ProgramCreateView.as_view(), name='program_new'),
    path('programs/<int:program_id>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('programs/<int:program_id>/edit', views.ProgramUpdateView.as_view(), name='program_edit'),
    path('programs/<int:program_id>/delete', views.ProgramDeleteView.as_view(), name='program_delete'),
    # Program - Drill
    path('programs/<int:program_id>/drills/add', , name='drill_add'), # ADD View
    path('programs/<int:program_id>/drills/<id_drill>/remove', ,name='drill_remove') # ADD View
    # Workout
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('workouts/new/', views.WorkoutCreateView.as_view(), name='workout_new'),
    path('workouts/<int:workout_id>', views.WorkoutDetailView.as_view(), name='workout_detail'),
    path('workouts/<int:workout_id>/edit', views.WorkoutUpdateView.as_view(), name='workout_edit'),
    path('workouts/<int:workout_id>/delete', views.WorkoutDeleteView.as_view(), name='workout_delete'),
    # Workout - Performance
    path('workout/<int:workout_id/Performances/new/', views.PerformanceCreateView.as_view(), name='performance_new'),
    path('workout/<int:workout_id/Performances/<int:performance_id>', views.PerformanceDetailView.as_view(), name='performance_detail'),
    path('workout/<int:workout_id/Performances/<int:performance_id>/edit', views.PerformanceUpdateView.as_view(), name='performance_edit'),
    path('workout/<int:workout_id/Performances/<int:performance_id>/delete', views.PerformanceDeleteView.as_view(), name='performance_delete'),
    # Email change
    path('change_profile', views.user_profile_change, name='user_profile_change'),
    # User attendance
    path('attendance', views.attendance, name='attendance'),
    # User attendance
    path('payments', views.payments, name='payments')
]
