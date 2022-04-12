import datetime
import time

from django.contrib import messages, admin
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
    raise_exception = True
    fields = '__all__'
    template_name = 'training/create_exercise.html'
    permission_required = 'training.add_exercises'
    success_url = reverse_lazy('training:create-exercise')
    success_message = 'Data Successfully added!'


class CreateTrainingView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    model = models.Training
    fields = ('name', 'description')
    template_name = 'training/create_training.html'
    permission_required = 'training.add_training'
    success_url = reverse_lazy('training:create-training')
    success_message = 'Data Successfully added!'
    raise_exception = True

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CreateTrainingPlanView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.TrainingPlan
    fields = ('exercise_name', 'order', 'training', 'number_of_sets', 'reps', 'reps_unit', 'pace_of_exercise',
              'rest_between_sets')

    template_name = 'training/create_training_plan.html'
    permission_required = 'training.add_trainingplan'
    success_url = reverse_lazy('training:create-training-plan')
    success_message = 'Data Successfully added!'
    raise_exception = True

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields['training'].queryset = form.fields['training'].queryset.filter(owner=self.request.user)
        return form


class ListTrainingPlanView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    model = models.TrainingPlan
    template_name = 'training/list.html'
    permission_required = 'training.view_trainingplan'
    login_url = reverse_lazy('users:login')
    raise_exception = True


class DetailExerciseView(DetailView):
    model = models.Exercises


class WorkoutView(CreateExerciseView):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    model = models.WorkoutSet
    fields = ('date', 'day', 'exercise', 'sets', 'reps', 'reps_unit', 'weight', 'total_weight', 'weight_unit')
    template_name = 'training/workout.html'
    permission_required = 'training.add_workoutset'
    success_url = reverse_lazy('training:workout-list')
    raise_exception = True

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class WorkoutUpdateView(SuccessMessageMixin, UpdateView):
    model = models.WorkoutSet
    fields = ('day', 'exercise', 'sets', 'reps', 'reps_unit', 'weight', 'total_weight', 'weight_unit')
    template_name = 'training/workoutset_list.html'
    success_url = reverse_lazy('training:workout-list')
    raise_exception = True
    success_message = 'Edit successfully!'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.date = time.strftime("%Y-%m-%d")
        return super().form_valid(form)


class WorkoutListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    model = models.WorkoutSet
    permission_required = 'training.view_workoutset'
    raise_exception = True
