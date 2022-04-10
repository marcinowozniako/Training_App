from django.contrib import admin

from . import models


@admin.register(models.Exercises)
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(models.DayName)
class DayAdmin(admin.ModelAdmin):
    list_display = ('day_name', 'order')


@admin.register(models.Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(models.TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = (
        'exercise_name',
        'order',
        'training',
        'day_name',
        'number_of_sets',
        'reps',
        'reps_unit',
        'pace_of_exercise',
        'rest_between_sets',
                    )
