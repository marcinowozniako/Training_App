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
    success_url = reverse_lazy('training:create-exercise')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


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
    permission_required = 'training_plan.add_training_plan'
    success_url = reverse_lazy('training:create-training-plan')


class ListTrainingPlanView(CreateTrainingPlanView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['planlist'] = models.TrainingPlan.objects.all().order_by('day_name__order', 'order')
        return ctx

    template_name = 'training/list.html'
    permission_required = 'training_plan.view_training_plan'
