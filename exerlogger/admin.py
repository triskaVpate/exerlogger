# Register your models here.

from django.contrib import admin

from .models import Drill, Exercise, Workout


class DrillAdmin(admin.ModelAdmin):
    list_display = ('created', 'name')
    list_filter = ()
    search_fields = ()
    date_hierarchy = 'created'


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('created', 'workout', 'drill', 'weight', 'round', 'repetition')
    list_filter = ()
    search_fields = ()
    date_hierarchy = 'created'


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('created', 'date', 'user')
    list_filter = ()
    search_fields = ()
    date_hierarchy = 'created'


admin.site.register(Drill, DrillAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Workout, WorkoutAdmin)
