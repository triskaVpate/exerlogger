from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.db.models import CharField

from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from datetime import date


# from phonenumber_field.modelfields import PhoneNumberField


class Drill(TimeStampedModel):
    name: CharField = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("drill")
        verbose_name_plural = _("drills")
        # unique_together = ()
        # index_together = ()

    objects = models.Manager()

    def __str__(self):
        return self.name


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
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+420123456789'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # validators should be a list
    # var number unique for every user will be used for payments
    var_num = models.IntegerField(_("var_num"), unique=True, null=True)

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


class Exercise(TimeStampedModel):
    workout = models.ForeignKey(Workout, verbose_name=_("workout"), on_delete=models.CASCADE)
    drill = models.ForeignKey(Drill, verbose_name=_("drill"), on_delete=models.SET("Drill no longer exists"))
    weight = models.IntegerField(_("weight"), blank=True, null=True)
    round = models.IntegerField(_("round"), default=1)
    repetition = models.IntegerField(_("repetition"), default=1)

    class Meta:
        verbose_name = _("exercise")
        verbose_name_plural = _("exercises")
        # unique_together = ()
        # index_together = ()

    def __string__(self):
        return self.workout


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