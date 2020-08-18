from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from exerlogger.models import (Exercise, Workout, CustomUser,
                               Performance, Drill, Program,
                               Exercise, Equipment, Property)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserEmailChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email']


class CustomUserAdvancedChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']

"""
Logging
"""
# Workout
class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ()


# Exercise
class ExerciseForm(forms.ModelForm):

    class Meta:
        model = Exercise
        fields = ('drill',)


# Performance
class PerformanceForm(forms.ModelForm):

    class Meta:
        model = Performance
        fields = ('equipment','sets','reps')


# Drill
class DrillForm(forms.ModelForm):

    class Meta:
        model = Drill
        fields = ('name', 'form', 'bilateral')  # There has to be a comma. Otherwise it's read a string not tuple as
        # it should be.


# Program
class ProgramForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = ('name', 'description', 'drills')
        widgets = {
            'drills': forms.CheckboxSelectMultiple,
        }


# Equipment
class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = ('name',)


# Property - Equipment
class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = ('name', 'unit', 'value')
