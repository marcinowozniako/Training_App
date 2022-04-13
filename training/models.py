from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from embed_video.fields import EmbedVideoField

from training.enums import Days, RepUnit, WeightUnit


class Exercises(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video = EmbedVideoField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class DayName(models.Model):
    day_name = models.SmallIntegerField(choices=Days.CHOICES)
    order = models.SmallIntegerField(unique=True)

    def __str__(self):
        return self.get_day_name_display()


class Training(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    exercises = models.ManyToManyField('Exercises', through='TrainingPlan')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class TrainingPlan(models.Model):
    exercise_name = models.ForeignKey('Exercises', on_delete=models.CASCADE)
    order = models.IntegerField()
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    number_of_sets = models.IntegerField(default=3)
    reps = models.PositiveIntegerField()
    reps_unit = models.CharField(max_length=25, choices=RepUnit.CHOICES)
    pace_of_exercise = models.CharField(max_length=4, blank=True)
    rest_between_sets = models.IntegerField()
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.exercise_name.name

    class Meta:
        ordering = ['training']


class WorkoutSet(models.Model):
    date = models.DateField(null=True, blank=True)
    day = models.ForeignKey('DayName', on_delete=models.CASCADE)
    exercise = models.ForeignKey('Exercises', on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    reps_unit = models.CharField(max_length=25, choices=RepUnit.CHOICES)
    weight = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    total_weight = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    weight_unit = models.CharField(max_length=15, choices=WeightUnit.CHOICES)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.exercise.name

    class Meta:
        ordering = ['date']


