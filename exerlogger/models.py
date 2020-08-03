from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
from django.db.models import CharField

from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from datetime import date


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


######################
### Logging System ###
######################

class Workout(TimeStampedModel):
    date = models.DateField(_("date"), default=date.today)
    user = models.ForeignKey(CustomUser, verbose_name=_("user"), on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = _("workout")
        verbose_name_plural = _("workouts")
        # unique_together = ()
        # index_together = ()w

    def __string__(self):
        return self.date


class Form(models.Model):
    """
    Each Drill can have Form.
    """
    name = models.CharField(max_length=256, unique=True)   # One form can be shared between one and more Drills thus it has to be unique.

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("form")
        verbose_name_plural = _("forms")


class Drill(TimeStampedModel):
    name: CharField = models.CharField(_("name"), max_length=255)
    bilateral = models.BooleanField()
    kb5_level = models.IntegerField(_("kb5_level"), null=True, blank=True)
    forms = models.ForeignKey(Form, related_name='forms', blank=True, on_delete=models.CASCADE)   # Drill can have a form, but doesn't have to.

    class Meta:
        verbose_name = _("drill")
        verbose_name_plural = _("drills")
        # unique_together = ()
        # index_together = ()

    objects = models.Manager()

    def __str__(self):
        return self.name


class Program(models.Model):
    """
    Each Workout can follow a Program.
    """
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    consists = models.ManyToManyField(Drill)

    def __str__(self):
        return self.name


class Exercise(TimeStampedModel):
    workout = models.ForeignKey(Workout, verbose_name=_("workout"), on_delete=models.CASCADE)
    drill = models.ForeignKey(Drill, verbose_name=_("drill"), on_delete=models.SET("Drill no longer exists"))

    class Meta:
        verbose_name = _("exercise")
        verbose_name_plural = _("exercises")
        # unique_together = ()
        # index_together = ()

    def __string__(self):
        return self.workout


class Property(models.Model):
    """
    Each Equipment can have one Property.
    """
    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=8)
    value = models.IntegerField()

    class Meta:
        verbose_name = _("property")
        verbose_name_plural = _("properties")


class Equipment(models.Model):
    """
    """
    property = models.ForeignKey(Property, verbose_name=_("property"), on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = _("equipment")
        verbose_name_plural = _("equipments")



class Performance(models.Model):
    """
    Each exercise is performed once and more with different Equipment.
    """
    exercise = models.ForeignKey(Exercise, verbose_name=_("exercise"), on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, verbose_name=_("equipment"), blank=True, on_delete=models.CASCADE)
    order = models.IntegerField()
    sets = models.IntegerField(_("round"), default=1)
    reps = models.IntegerField(_("repetition"), default=1)
