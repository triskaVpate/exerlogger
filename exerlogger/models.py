from django.contrib.auth.models import User
from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from datetime import date


class Drill(TimeStampedModel):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("drill")
        verbose_name_plural = _("drills")
        # unique_together = ()
        # index_together = ()

    objects = models.Manager()

    def __unicode__(self):
        return self.get_name_display()

    def __str__(self):
        return self.name


class Workout(TimeStampedModel):
    date = models.DateField(_("date"), default=date.today)
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = _("workout")
        verbose_name_plural = _("workouts")
        # unique_together = ()
        # index_together = ()

    def __unicode__(self):
        return self.date

class Exercise(TimeStampedModel):
    workout = models.ForeignKey(Workout, verbose_name=_("workout"), on_delete=models.CASCADE)
    drill = models.ForeignKey(Drill, verbose_name=_("drill"), on_delete=models.CASCADE)
    weight = models.IntegerField(_("weight"), blank=True, null=True)
    round = models.IntegerField(_("round"))
    repetition = models.IntegerField(_("repetition"))

    class Meta:
        verbose_name = _("exercise")
        verbose_name_plural = _("exercises")
        # unique_together = ()
        # index_together = ()

    def __unicode__(self):
        return self.workout
