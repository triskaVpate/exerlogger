from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
from django.db.models import CharField

from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from datetime import date

from django.urls import reverse

class Gym(TimeStampedModel):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("gym")
        verbose_name_plural = _("gyms")
        # unique_together = ()
        # index_together = ()

    objects = models.Manager()

    def __str__(self):
        return self.name


# Lesson is used here as a school class, but the name 'class' would be very confusing
class Lesson(TimeStampedModel):
    name = models.CharField(_("name"), max_length=255)
    weekdays = models.CharField(_("weekdays"), max_length=255)
    begins_at = models.IntegerField(_("begins_at"), blank=True, null=True)
    gym = models.ForeignKey(Gym, verbose_name=_("gym"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("lesson")
        verbose_name_plural = _("lessons")
        # unique_together = ()
        # index_together = ()

    objects = models.Manager()  # TODO ??? proc to tu je?

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    pass
    # email field should be unique in db
    email = models.EmailField(_('email address'), blank=True, unique=True)
    # add additional fields in here
    lesson = models.ForeignKey(Lesson, verbose_name=_("lesson"), on_delete=models.SET_NULL, blank=True, null=True)
    # taking care of phone number
    phone_regex = RegexValidator(regex=r'^\+\d{12}$',
                                 message="Phone number must be entered in the format: +420123456789.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    # var number unique for every user will be used for payments
    var_num = models.IntegerField(_("var_num"), unique=True, null=True)
    # list of months user paid for
    membership = JSONField(_('membership'), null=True, blank=True)

    def __str__(self):
        return self.username


# Training is a instance of a class/lesson taking place at particular day/hour
class Training(TimeStampedModel):
    date = models.DateField(_("date"), default=date.today)
    lesson = models.ForeignKey(Lesson, verbose_name=_("lesson"), on_delete=models.SET("Lesson no longer exists"))
    participants = models.ManyToManyField(CustomUser)

    class Meta:
        verbose_name = _("training")
        verbose_name_plural = _("trainings")
        # unique_together = ()
        # index_together = ()

    def __str__(self):
        return str(self.date)


class Payment(TimeStampedModel):
    date = models.DateField(_("date"), default=date.today)
    money = models.DecimalField(max_digits=6, decimal_places=2)
    var_num = models.IntegerField(_("var_num"), null=True)

    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")
        # unique_together = ()
        # index_together = ()w

    def __string__(self):
        return self.date


"""
Logging
"""

class Workout(TimeStampedModel):
    """
    Attributes:
        date(date): The date when the Workout was created.
                    Today is set as default.
        user(FK): The User who performed the Workout.
                  When User is deleted all his Workouts are deleted (CASCADE).

    Relation:
        Each Workout belongs to one User.
        User can perform one and more Workouts.
    """
    date = models.DateField(_("date"), default=date.today)
    user = models.ForeignKey(CustomUser, verbose_name=_("user"), on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = _("workout")
        verbose_name_plural = _("workouts")
        # unique_together = ()
        # index_together = ()w

    def get_absolute_url(self):
        return reverse('workout_detail',kwargs={'workout_id':self.pk})

    def __string__(self):
        return self.date


class Form(models.Model):
    """
    Attributes:
        name(str): Name of the form. It must be unique, which ensures reuseability.

    Relation:
        Each Form belongs to one and more Drills.

    Example:
        Onearm (Drill.form.name) Swing (Drill.name)
        Onearm (Drill.form.name) Deadlift (Drill.name)
    """
    name = models.CharField(max_length=256, unique=True)   # One form can be shared between one and more Drills thus it has to be unique.

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("form")
        verbose_name_plural = _("forms")


class Drill(TimeStampedModel):
    """
    Attributes:
        name(str): Name of the Drill.
        kb5_level(int): Minimum KB5 level that you have to reach in order to practise this Drill.
        form(FK): Form of the Exercise. It's optional.
        bilateral(bool): True if both limbs are used in unison to contract the muscles.
                         False if is when each limb works independently of the other
                         to create the desired movement.

    Relation:
        Each Drill can have a Form.

    Example:
        Onearm (Drill.form.name) Swing (Drill.name)
    """

    name: CharField = models.CharField(_("name"), max_length=255)
    kb5_level = models.IntegerField(_("kb5_level"), null=True, blank=True)
    form = models.ForeignKey(Form, related_name='forms', blank=True, on_delete=models.CASCADE, null=True)   # Drill can have a form, but doesn't have to.
    bilateral = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("drill")
        verbose_name_plural = _("drills")
        # unique_together = ()
        # index_together = ()

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('drill_detail',kwargs={'drill_id':self.pk})

    def __str__(self):
        return self.name


class Program(models.Model):
    """
    Attributes:
        name(str): Name of the Program.
        description(str): Description of the Program.
        consists(MTM): Table which stores which Drills are performed during the Program.

    Relation:
        Each Workout can follow a Program.

    Example:
        Simple and Sinister Full body program(Program.name) consists(Program.consists)
        of Onearm Swing, Snatch and Pull Ups. It's great for advanced ... (Program.description)
    """
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    drills = models.ManyToManyField(Drill)

    def get_absolute_url(self):
        return reverse('program_detail',kwargs={'program_id':self.pk})

    def __str__(self):
        return self.name


class Exercise(TimeStampedModel):
    """
    Attributes:
        workout(FK): Workout to which this Exercise belongs.
        drill(FK): Drill which is performed during this Exercise.

    Relation:
        During each Exercise User performs a Drill.
        Each Exercise belongs to a Workout.
    """
    workout = models.ForeignKey(Workout, verbose_name=_("workout"), related_name='exercises', on_delete=models.CASCADE)
    drill = models.ForeignKey(Drill, verbose_name=_("drill"), on_delete=models.SET("Drill no longer exists"))

    class Meta:
        verbose_name = _("exercise")
        verbose_name_plural = _("exercises")
        # unique_together = ()
        # index_together = ()

    """
    def get_absolute_url(self):
        return reverse('exercise_detail',kwargs={'exercise_id':self.pk})
    """

    def __str__(self):
        return self.drill.name


class Equipment(models.Model):
    """
    Attributes:
        name(str): Name of the Equipment. It doesn't have to be unique.

    Relation:
        Each Exercise can be Performed with an Equipment.

    Example:
        Kettlebell(Equipment.name)
    """
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = _("equipment")
        verbose_name_plural = _("equipments")

    def get_absolute_url(self):
        return reverse('equipment_detail',kwargs={'equipment_id':self.pk})

    def __str__(self):
        if hasattr(self, 'property'):
            return "{} ({}{})".format(self.name, self.property.value, self.property.unit)
        else:
            return self.name


class Property(models.Model):
    """
    Attributes:
        equipment(FK): Equipment this Property belongs.
        name(str): Name of the Property.
        unit(str): Unit in which that Property is measured.
        value(int): Value of the Property.

    Relation:
        Each Equipment can have a Property.

    Example:
        Kettlebell(Equipment.name) has weight(Property.name) of 20(Property.value)Kg(Property.unit)
        Stool(Equipment.name) has a height(Property.name) of 30(Property.value)cm(Property.unit)
    """
    equipment = models.OneToOneField(Equipment, verbose_name=_("equipment"), related_name='property', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=8)
    value = models.IntegerField()

    class Meta:
        verbose_name = _("property")
        verbose_name_plural = _("properties")

    def __str__(self):
        return self.name + str(self.value) + self.unit


class Performance(models.Model):
    """
    Attributes:
        exercise(FK): Exercise this Performance belongs.
        equipment(FK): Equipment that has been used.
        sets(int): Number of Performed sets.
        reps(int): Number of Performed reps.

    Relation:
        Each Exercise is Performed once and more times with different Equipment.
        and different number of times.

    Example:
        Swing(Performance.exercise.drill.name) is Performed 1(Performance.order)st time
        2(Performance.sets) sets of 5(Performance.reps) reps
        with kettlebell(Performance.eqipment.name) during (Performance.workout)

        Swing(Performance.exercise.drill.name) is Performed 2(Performance.order)nd
        time 1(Performance.sets) sets of 7(Performance.reps) reps
        with kettlebell(Performance.eqipment.name) during (Performance.workout)
    """
    exercise = models.ForeignKey(Exercise, verbose_name=_("exercise"), related_name='performances',
                                 on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, verbose_name=_("equipment"), blank=True, on_delete=models.CASCADE,
                                  null=True)
    sets = models.IntegerField(_("sets"), default=1)
    reps = models.IntegerField(_("reps"), default=1)

    def get_absolute_url(self):
        return reverse('workout_detail', kwargs={'performance_id': self.pk})
