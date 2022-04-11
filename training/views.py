from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from . import models


class CreateExerciseView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Exercises
    fields = '__all__'
    template_name = 'training/create_exercise.html'
    permission_required = 'training.add_exercises'
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy('training:create-exercise')
    success_message = 'Data Successfully added!'


class CreateTrainingView(CreateExerciseView):
    model = models.Training
    fields = ('name', 'description')
    template_name = 'training/create_training.html'
    permission_required = 'training.add_training'
    success_url = reverse_lazy('training:create-training')


class CreateTrainingPlanView(CreateExerciseView):
    model = models.TrainingPlan
    fields = '__all__'
    template_name = 'training/create_training_plan.html'
    permission_required = 'training.add_trainingplan'
    success_url = reverse_lazy('training:create-training-plan')


class ListTrainingPlanView(ListView):
    model = models.TrainingPlan
    template_name = 'training/list.html'
    permission_required = 'training.view_trainingplan'


class DetailExerciseView(DetailView):
    model = models.Exercises


class WorkoutView(CreateExerciseView):
    model = models.WorkoutSet
    fields = '__all__'
    template_name = 'training/workout.html'
    permission_required = 'training.add_workoutset'
    success_url = reverse_lazy('training:workout-list')


class WorkoutUpdateView(UpdateView):
    model = models.WorkoutSet
    fields = '__all__'
    template_name = 'training/workoutset_list.html'


class WorkoutListView(ListView):
    model = models.WorkoutSet
