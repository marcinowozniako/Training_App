from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView, WeekArchiveView
from django.views.generic.edit import FormMixin
from extra_views import ModelFormSetView, CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory, \
    FormSetView

from . import models


class CreateExerciseView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    model = models.Exercises
    raise_exception = True
    fields = '__all__'
    template_name = 'training/create_exercise.html'
    permission_required = 'training.add_exercises'
    success_url = reverse_lazy('training:create-exercise')
    success_message = 'Data Successfully added!'


class CreateTrainingView(CreateExerciseView):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    model = models.Training
    fields = ('name', 'description')
    template_name = 'training/create_training.html'
    permission_required = 'training.add_training'
    success_url = reverse_lazy('training:create-training')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CreateTrainingPlanView(CreateExerciseView):
    model = models.TrainingPlan
    fields = (
        'training_plan_nb', 'exercise_name', 'order', 'training', 'number_of_sets', 'reps', 'reps_unit',
        'pace_of_exercise',
        'rest_between_sets',)

    template_name = 'training/create_training_plan.html'
    permission_required = 'training.add_trainingplan'
    success_url = reverse_lazy('training:create-training-plan')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields['training'].queryset = form.fields['training'].queryset.filter(owner=self.request.user)
        form.fields['order'].widget = forms.NumberInput(attrs={'min': 1})
        form.fields['training_plan_nb'].widget = forms.NumberInput(attrs={'min': 1})
        return form


class ListTrainingPlanView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user).order_by('training', 'order')

    model = models.TrainingPlan
    template_name = 'training/list.html'
    permission_required = 'training.view_trainingplan'
    login_url = reverse_lazy('users:login')
    raise_exception = True

    # form_class = forms.E
    #
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['training_id'] = models.TrainingPlan.objects.filter(owner=self.request.user, training_plan_nb_id=2).order_by(
            'training', 'order')
        ctx['current_plan'] = models.TrainingPlan.objects.filter(owner=self.request.user, training_plan_nb_id=1).first()
        return ctx


class TrainingPlanChoiceView(ModelFormSetView):
    def get_queryset(self):
        return self.model.objects.filter(id=1)
    model = models.TrainingPlanName
    fields = ('training_plan_name',)


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
    success_url = reverse_lazy('training:workout')
    raise_exception = True

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date'].widget = forms.TextInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class WorkoutUpdateView(SuccessMessageMixin, UpdateView):
    model = models.WorkoutSet
    fields = ('day', 'exercise', 'sets', 'reps', 'reps_unit', 'weight', 'total_weight', 'weight_unit')
    template_name = 'training/workoutset_list.html'
    raise_exception = True
    success_message = 'Edit successfully!'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['id'] = self.request.META['HTTP_REFERER']
        return ctx

    def get_success_url(self):
        self.success_url = self.request.POST.get('next')
        return self.success_url.format(**self.object.__dict__)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class WorkoutListView(WeekArchiveView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user).order_by('date', 'exercise__training',
                                                                           'exercise__trainingplan__order')

    model = models.WorkoutSet
    permission_required = 'training.view_workoutset'
    raise_exception = True
    template_name = 'training/workoutset_list.html'
    week_format = '%W'
    date_field = 'date'
    allow_future = True
    allow_empty = True


class DeleteExerciseWorkoutView(SuccessMessageMixin, DeleteView):
    model = models.WorkoutSet
    success_message = 'Delete successfully!'
    template_name = 'training/trainingplan_confirm_delete.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['id'] = self.request.META['HTTP_REFERER']
        return ctx

    def get_success_url(self):
        self.success_url = self.request.POST.get('next')
        return self.success_url.format(**self.object.__dict__)
