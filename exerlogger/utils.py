from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Workout


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter workouts by day
    def formatday(self, day, workouts):
        workouts_per_day = workouts.filter(date__day=day)
        d = ''
        for workout in workouts_per_day:
            d += f'<li> {workout.id} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, workouts):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, workouts)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter workouts by year and month
    def formatmonth(self, withyear=True):
        workouts = Workout.objects.filter(date__year=self.year, date__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, workouts)}\n'
        return cal
