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
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from exerlogger import views
from exerlogger.views import user_homepage


app_name = 'exerlogger'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

#user homepage
    path('', user_homepage, name='home'),
#user workouts list
    path('workouts/', views.workouts, name='workouts'),
# create new workout page
    path('workouts/add/', views.workout_detail, name='workout_new'),
# workout exercises list
    path('workouts/<int:workout_id>/', views.workout_detail, name='workout_detail'),
#edit exercise in workout
    path('workouts/<int:workout_id>/<int:exercise_id>', views.workout_detail, name='exercise_edit')
]
