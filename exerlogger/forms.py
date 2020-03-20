from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from exerlogger.models import Exercise, Workout, CustomUser


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


class NewWorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ["date"]


class NewExerciseForm(forms.ModelForm):

    class Meta:
        model = Exercise
        fields = ["drill", "weight", "round", "repetition"]


class CustomUserAdvancedChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']
