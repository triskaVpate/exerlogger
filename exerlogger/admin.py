# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# custom auth model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Drill, Exercise, Workout, CustomUser, Gym, Lesson, Training
# used for fieldsets
from django.utils.translation import ugettext_lazy as _


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


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'groups_']
# fieldsets are used for choosing what should be visible in admin page
# I used it here to hide access rights setup
    fieldsets = (
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        # (_('Training attendance'), {'fields': ('training',)})
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'password1', 'password2'),
    #     }),
    # )

    def groups_(self, obj):
        return ", ".join(
            group.name for group in obj.groups.all()
        )

    # def trainings_(self, obj):
    #     return ", ".join(
    #         training.id for training in obj.training.all()
    #     )


class GymAdmin(admin.ModelAdmin):
    list_display = ('created', 'name')
    list_filter = ()
    search_fields = ()
    date_hierarchy = 'created'


class LessonAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'weekdays', 'begins_at', 'gym')
    list_filter = ()
    search_fields = ()
    date_hierarchy = 'created'


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('created', 'date', 'lesson', 'users_')
    list_filter = ()
    search_fields = ()
    date_hierarchy = 'created'

    def users_(self, obj):
        return ", ".join(
            user.username for user in obj.users.all()
        )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Drill, DrillAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Gym, GymAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Training, TrainingAdmin)