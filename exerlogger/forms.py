from django import forms
from django.forms import inlineformset_factory

from exerlogger.models import Exercise, Workout


class NewWorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ["date"]


class NewExerciseForm(forms.ModelForm):

    class Meta:
        model = Exercise
        fields = ["drill", "weight", "round", "repetition"]


#NewExerciseFormSet = inlineformset_factory(Workout, Exercise, form=NewExerciseForm, extra=1, can_delete=True)
