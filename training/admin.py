from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from . import models


@admin.register(models.Exercises)
class ExercisesAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ('name', 'description', 'video')


@admin.register(models.DayName)
class DayAdmin(admin.ModelAdmin):
    list_display = ('day_name', 'order')


@admin.register(models.Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner',)


@admin.register(models.TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = (
        'exercise_name',
        'order',
        'training',
        'number_of_sets',
        'reps',
        'reps_unit',
        'pace_of_exercise',
        'rest_between_sets',
        'owner',
    )


@admin.register(models.WorkoutSet)
class WorkoutSetAdmin(admin.ModelAdmin):
    list_display = (
        'sets',
        'reps',
        'reps_unit',
        'weight',
        'total_weight',
        'weight_unit',
        'day',
        'exercise',
        'date',
        'owner',
    )

