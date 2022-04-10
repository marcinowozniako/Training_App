from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import models


class CreateExerciseView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Exercises
    fields = '__all__'
    template_name = 'training/create_exercise.html'
    permission_required = 'exercises.add_exercise'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CreateTrainingView(CreateExerciseView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Training
    fields = ('name', 'description')
    template_name = 'training/create_training.html'
    permission_required = 'training.add_training'

