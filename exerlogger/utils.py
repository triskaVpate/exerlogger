from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Workout, Training


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter workouts by day
    def formatday(self, day, workouts, trainings, username):
        workouts_per_day = workouts.filter(date__day=day, user=username)
        trainings_per_day = trainings.filter(date__day=day)
        d = ''
        for workout in workouts_per_day:
            # TODO im not usre about the hardcoded url but i could figure out how to do django do his thing
            d += f'''<li><a href="workouts/{workout.id}">Workout {workout.id }</a> </li>'''

        # attempt for KB5 trainings coloring
        for training in trainings_per_day:
            if username in training.participants.all():
                d += f'''<div id="attendance_ok"><li>KB5 {training.lesson}</li></div>'''
            else:
                d += f'''<div id="attendance_absent"><li>KB5 {training.lesson}</li></div>'''

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, workouts, trainings, username):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, workouts, trainings, username=username)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter workouts by year and month
    def formatmonth(self, username, withyear=True):
        workouts = Workout.objects.filter(date__year=self.year, date__month=self.month, user=username)
        trainings = Training.objects.filter(date__year=self.year, date__month=self.month, lesson=username.lesson)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, workouts, trainings, username=username)}\n'
        return cal
