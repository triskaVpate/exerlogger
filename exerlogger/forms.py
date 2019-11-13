from datetime import date

from django import forms

from exerlogger.models import Exercise, Drill, Workout


class NewWorkoutForm(forms.ModelForm):
    #workout_date = forms.DateField(required=True, initial=date.today())

    class Meta:
        model = Workout
        fields = ["date"]

class NewExerciseForm(forms.ModelForm):
    drill = forms.ModelChoiceField(queryset=Drill.objects.all(), initial=0)
    weight = forms.IntegerField()

    class Meta:
        model = Exercise
        fields = ["drill", "weight"]
