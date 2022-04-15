import datetime
import time
from datetime import timedelta, date

import django_select2
from django import forms
from django.contrib import messages, admin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView, WeekArchiveView
from django.views.generic.dates import WeekMixin
from django_select2.forms import Select2Widget

from . import models
from .models import WorkoutSet


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
        return self.model.objects.filter(owner=self.request.user).order_by('training', 'order')

    model = models.TrainingPlan
    template_name = 'training/list.html'
    permission_required = 'training.view_trainingplan'
    login_url = reverse_lazy('users:login')
    raise_exception = True


class TrainingPlanUpdateView(SuccessMessageMixin, UpdateView):
    model = models.TrainingPlan
    fields = ('exercise_name', 'order', 'training', 'number_of_sets', 'reps', 'reps_unit', 'pace_of_exercise',
              'rest_between_sets')
    success_message = 'Edit successfully!'
    success_url = reverse_lazy('training:list')
    template_name = 'training/list.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DeleteTrainingPlanView(SuccessMessageMixin, DeleteView):
    model = models.TrainingPlan
    success_url = reverse_lazy('training:list')
    success_message = 'Delete successfully!'


class DetailExerciseView(DetailView):
    model = models.Exercises


class UpdateExerciseView(SuccessMessageMixin, UpdateView):
    model = models.Exercises
    fields = '__all__'
    success_message = 'Edit successfully!'
    success_url = reverse_lazy('training:list')


class WorkoutView(CreateExerciseView):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    model = models.WorkoutSet
    fields = ('date', 'day', 'exercise', 'sets', 'reps', 'reps_unit', 'weight', 'total_weight', 'weight_unit')
    template_name = 'training/workout.html'
    permission_required = 'training.add_workoutset'
    success_url = reverse_lazy('training:workout-list')
    raise_exception = True

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date'].widget = forms.TextInput(attrs={'type': 'date'})
        # form.fields['exercise'].widget = Select2Widget
        return form

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
        return super().form_valid(form)


class WorkoutListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user).order_by('date', 'exercise__training',
                                                                           'exercise__trainingplan__order')

    model = models.WorkoutSet
    permission_required = 'training.view_workoutset'
    raise_exception = True
    paginate_by = 7


class DeleteExerciseWorkoutView(SuccessMessageMixin, DeleteView):
    model = models.WorkoutSet
    success_message = 'Delete successfully!'
    template_name = 'training/trainingplan_confirm_delete.html'
    success_url = reverse_lazy('training:workout-list')
