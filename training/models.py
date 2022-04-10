from django.db import models

from training.enums import Days, RepUnit


class Exercises(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

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

    def __str__(self):
        return self.name


class TrainingPlan(models.Model):
    exercise_name = models.ForeignKey('Exercises', on_delete=models.CASCADE)
    order = models.IntegerField()
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    day_name = models.ForeignKey('DayName', on_delete=models.CASCADE)
    number_of_sets = models.IntegerField(default=3)
    reps = models.PositiveIntegerField()
    reps_unit = models.CharField(max_length=2, choices=RepUnit.CHOICES)
    pace_of_exercise = models.CharField(max_length=4)
    rest_between_sets = models.IntegerField()

    def __str__(self):
        return self.exercise_name.name
