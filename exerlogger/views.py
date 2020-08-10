from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.safestring import mark_safe

from exerlogger.forms import (CustomUserCreationForm, CustomUserChangeForm,
                              CustomUserEmailChangeForm, CustomUserAdvancedChangeForm,
                              WorkoutForm, PerformanceForm,
                              DrillForm, ProgramForm, ExerciseForm)
from .models import (Exercise, Workout, CustomUser,
                     Training, Payment, Program,
                     Performance, Drill, Exercise)
from .utils import Calendar
# from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
# Class Based Views imports
from django.views import View
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


@login_required
def payments(request):
    user_payments = Payment.objects.filter(var_num=request.user.var_num).order_by('-date')
    user_membership = request.user.membership

    if type(user_membership) is dict:
        user_membership = user_membership['2020']

    months_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    context = {'user_payments': user_payments, 'months_list': months_list, 'user_membership': user_membership}
    return render(request, 'payments/payments.html', context)


@login_required
def attendance(request):
    # list of training sessions for loging that user is present or missing
    user_trainings = request.user.training_set.all()
    list_user_trainings = []
    for training in user_trainings:
        list_user_trainings.append(training.id)
    all_trainings = Training.objects.filter(lesson=request.user.lesson).order_by('-date')
    context = {'user_trainings': user_trainings, 'list_user_trainings': list_user_trainings,
               'all_trainings': all_trainings}

    # calendar part
    d = datetime.date.today()

    # calendar movement start
    move = request.GET.get('move', None)
    month_id = request.GET.get('month_id', None)
    year_id = request.GET.get('year_id', None)

    if month_id is not None and move == "previous_month":
        d = d.replace(month=int(month_id))+relativedelta(months=-1, year=int(year_id))
    elif month_id is not None and move == "next_month":
        d = d.replace(month=int(month_id))+relativedelta(months=+1, year=int(year_id))
    # calendar movement end

    cal = Calendar(d.year, d.month)

    # Call the formatmonth method, which returns our calendar as a table
    html_cal = cal.formatmonth(withyear=True, username=request.user)
    context['calendar'] = mark_safe(html_cal)
    # this exist cause of moving to different months
    context['month_id'] = d.month
    context['year_id'] = d.year

    return render(request, 'attendance/attendance.html', context)


@login_required
def user_profile_change(request):
    user = get_object_or_404(CustomUser, username=request.user)
    # form = CustomUserEmailChangeForm(request.POST or None, instance=user)
    form = CustomUserAdvancedChangeForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save(commit=True)
        return redirect(user_profile_change)

    context = {'form': form, 'user': user}
    return render(request, 'registration/profile_change_form.html', context)


@login_required
def user_homepage(request):
    # which lesson is user member of
    # user_lesson =

    context = {}

    return render(request, 'userspace/index.html', context)


def signup_view(request):
    # show empty form
    form = CustomUserCreationForm()
    # if post, do the thing
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # after save lets authenticate user, login him and redirect to homepage
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'signup.html', {'form': form})


"""
Logging
"""
# Program
## List - Program
class ProgramListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Program
    template_name = 'exerlogger/logging/program_list.html'


## Create - Program
class ProgramCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Program
    redirect_field_name = 'exerlogger/logging/program_detail.html'
    form_class = ProgramForm
    template_name = 'exerlogger/logging/program_form.html'


## Detail - Program
class ProgramDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Program
    pk_url_kwarg = 'program_id'
    template_name = 'exerlogger/logging/program_detail.html'


## Update - Program
class ProgramUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Program
    redirect_field_name = 'exerlogger/logging/program_detail.html'
    form_class = ProgramForm
    pk_url_kwarg = 'program_id'
    template_name = 'exerlogger/logging/program_form.html'

## Delete - Program
class ProgramDeleteView(LoginRequiredMixin, DeleteView):
    model = Program
    success_url = reverse_lazy('program_list')
    pk_url_kwarg = 'program_id'
    template_name = 'exerlogger/logging/program_confirm_delete.html'


# Workout
# List - Workout
class WorkoutListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Workout
    template_name = 'exerlogger/logging/workout_list.html'


## Create - Workout
class WorkoutCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Workout
    redirect_field_name = 'exerlogger/logging/workout_detail.html'
    form_class = WorkoutForm
    pk_url_kwarg = 'workout_id'
    template_name = 'exerlogger/logging/workout_form.html'


## Detail - Workout
class WorkoutDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Workout
    pk_url_kwarg = 'workout_id'
    template_name = 'exerlogger/logging/workout_detail.html'


## Update - Workout
class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Workout
    redirect_field_name = 'exerlogger/logging/workout_detail.html'
    form_class =WorkoutForm
    pk_url_kwarg = 'workout_id'
    template_name = 'exerlogger/logging/workout_form.html'


## Delete - Workout
class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Workout
    success_url = reverse_lazy('workout_list')
    pk_url_kwarg = 'workout_id'
    template_name = 'exerlogger/logging/workout_confirm_delete.html'

# Exercise
## List - Exercise
class ExerciseListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Exercise
    template_name = 'exerlogger/logging/exercise_list.html'


## Create - Exercise
class ExerciseCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Exercise
    redirect_field_name = 'exerlogger/logging/exercise_detail.html'
    form_class = ExerciseForm
    template_name = 'exerlogger/logging/exercise_form.html'

    def form_valid(self, form):
        # Get Workout id store it in form
        form.instance.workout = get_object_or_404(Workout, pk=self.kwargs['workout_id'])
        return super(ExerciseCreateView, self).form_valid(form)


## Detail - Exercise
class ExerciseDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Exercise
    pk_url_kwarg = 'exercise_id'
    template_name = 'exerlogger/logging/exercise_detail.html'


## Update - Exercise
class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Exercise
    redirect_field_name = 'exerlogger/logging/exercise_detail.html'
    form_class = ExerciseForm
    pk_url_kwarg = 'exercise_id'
    template_name = 'exerlogger/logging/exercise_form.html'


## Delete - Exercise
class ExerciseDeleteView(LoginRequiredMixin, DeleteView):
        model = Exercise
        success_url = reverse_lazy('exercise_list')
        pk_url_kwarg = 'exercise_id'
        template_name = 'exerlogger/logging/exercise_confirm_delete.html'


# Performance
## Create - Performance
class PerformanceCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Performance
    redirect_field_name = 'exerlogger/logging/performance_detail.html'
    form_class = PerformanceForm
    template_name = 'exerlogger/logging/performance_form.html'


## Detail - Performance
class PerformanceDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Performance
    pk_url_kwarg = 'performance_id'
    template_name = 'exerlogger/logging/performance_detail.html'


## Update - Performance
class PerformanceUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Performance
    redirect_field_name = 'exerlogger/logging/performance_detail.html'
    form_class = PerformanceForm
    pk_url_kwarg = 'performance_id'
    template_name = 'exerlogger/logging/performance_form.html'


## Delete - Performance
class PerformanceDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Performance
    success_url = reverse_lazy('performance_list')
    pk_url_kwarg = 'performance_id'
    template_name = 'exerlogger/logging/performance_confirm_delete.html'


# Drill
## List - Drill
class DrillListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Drill
    template_name = 'exerlogger/logging/drill_list.html'


## Create - Drill
class DrillCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Drill
    redirect_field_name = 'exerlogger/logging/drill_detail.html'
    form_class = DrillForm
    template_name = 'exerlogger/logging/drill_form.html'


## Detail - Drill
class DrillDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Drill
    pk_url_kwarg = 'drill_id'
    template_name = 'exerlogger/logging/drill_detail.html'


## Update - Drill
class DrillUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Drill
    redirect_field_name = 'exerlogger/logging/drill_detail.html'
    form_class = DrillForm
    pk_url_kwarg = 'drill_id'
    template_name = 'exerlogger/logging/drill_form.html'


## Delete - Drill
class DrillDeleteView(LoginRequiredMixin, DeleteView):
    model = Drill
    success_url = reverse_lazy('drill_list')
    pk_url_kwarg = 'drill_id'
    template_name = 'exerlogger/logging/drill_confirm_delete.html'
