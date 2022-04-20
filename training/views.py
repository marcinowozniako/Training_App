from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView, WeekArchiveView

from . import models, filters


class BaseCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    """
    Base class for every another CreateView
    """

    raise_exception = True
    success_message = 'Data Successfully added!'


class CreateExerciseView(BaseCreateView):
    """
    View for creating a new exercise object, with a response rendered by a template.
    Verify that the current user has all specified permissions.
    """
    model = models.Exercises
    fields = '__all__'
    template_name = 'training/create_exercise.html'
    success_url = reverse_lazy('training:create-exercise')
    permission_required = 'training.add_exercises'


class CreateTrainingView(BaseCreateView):
    """
    View for creating a new training object, with a response rendered by a template.
    Verify that the current user has all specified permissions.
    If the form is valid, add the current logged user as owner and redirect to the supplied URL.
    """
    model = models.Training
    fields = ('name', 'description')
    template_name = 'training/create_training.html'
    permission_required = 'training.add_training'
    success_url = reverse_lazy('training:create-training')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CreateTrainingPlanNameView(BaseCreateView):
    """
    View for creating a new training plan object, with a response rendered by a template.
    Verify that the current user has all specified permissions.
    If the form is valid, add the current logged user as owner and redirect to the supplied URL.
    """
    model = models.TrainingPlanName
    fields = ('training_plan_name',)
    permission_required = 'training.add_trainingplanname'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CreateTrainingPlanView(BaseCreateView):
    """
    View for creating a new training plan object, with a response rendered by a template. Verify that the current
    user has all specified permissions. If the form is valid, add the current logged user as owner and redirect to
    the supplied URL. Adds custom filtering for choice field of training and training_plan_name, listing only those
    created by current logged user, add min value for order field.
    """
    model = models.TrainingPlan
    fields = (
        'training_plan_name', 'exercise_name', 'order', 'training', 'number_of_sets', 'reps', 'reps_unit',
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
        form.fields['training_plan_name'].queryset = form.fields['training_plan_name'].queryset.filter(
            owner=self.request.user)
        form.fields['order'].widget = forms.NumberInput(attrs={'min': 1})
        return form


class ListTrainingPlanView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Render list of Training Plan objects, set by current logged user
    order by training id and exercises order.
    User can choose between all his training plans
    Verify that the current
    user has all specified permissions.
    """
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user).order_by('training', 'order')

    model = models.TrainingPlan
    template_name = 'training/list.html'
    permission_required = 'training.view_trainingplan'
    login_url = reverse_lazy('users:login')
    raise_exception = True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['filter'] = filters.SnippetFilter(self.request.GET, request=self.request, queryset=self.get_queryset())
        return ctx


class TrainingPlanUpdateView(SuccessMessageMixin, UpdateView):
    """
    View for updating an object, with a response rendered by a template.
    If the form is valid, add the current logged user as owner and redirect to
    the previous URL .
    """
    model = models.TrainingPlan
    fields = ('exercise_name', 'order', 'training', 'number_of_sets', 'reps', 'reps_unit', 'pace_of_exercise',
              'rest_between_sets')
    success_message = 'Edit successfully!'
    template_name = 'training/list.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['id'] = self.request.META['HTTP_REFERER']
        return ctx

    def get_success_url(self):
        self.success_url = self.request.POST.get('next')
        return self.success_url.format(**self.object.__dict__)


class DeleteTrainingPlanView(SuccessMessageMixin, DeleteView):
    """
    View for deleting an object retrieved with self.get_object(), with a
    response rendered by a template.
    """
    model = models.TrainingPlan
    success_url = reverse_lazy('training:list')
    success_message = 'Delete successfully!'


class DetailExerciseView(DetailView):
    """
    Render a "detail" view of an object.
    """
    model = models.Exercises


class UpdateExerciseView(SuccessMessageMixin, UpdateView):
    """
    View for updating an object, with a response rendered by a template.
    Add current url of site to context and redirect to
    the previous URL after successfully edit .
    """

    model = models.Exercises
    fields = '__all__'
    success_message = 'Edit successfully!'
    success_url = reverse_lazy('training:list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['id'] = self.request.META['HTTP_REFERER']
        return ctx

    def get_success_url(self):
        self.success_url = self.request.POST.get('next')
        return self.success_url.format(**self.object.__dict__)


class WorkoutView(BaseCreateView):
    """
    View for creating a new workout object, with a response rendered by a template.
    Verify that the current user has all specified permissions.
    Change the type of field date for date.
    If the form is valid, add the current logged user as owner and redirect to the supplied URL.
    """
    model = models.WorkoutSet
    fields = ('date', 'day', 'exercise', 'sets', 'reps', 'reps_unit', 'weight', 'total_weight', 'weight_unit')
    template_name = 'training/workout.html'
    permission_required = 'training.add_workoutset'
    success_url = reverse_lazy('training:workout')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date'].widget = forms.TextInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class WorkoutUpdateView(SuccessMessageMixin, UpdateView):
    """
    View for updating an object, with a response rendered by a template.
    Change the type of field date for date.
    If the form is valid, add the current logged user as owner.
    Add current url of site to context and redirect to
    the previous URL after successfully edit .
    """
    model = models.WorkoutSet
    fields = ('date', 'day', 'exercise', 'sets', 'reps', 'reps_unit', 'weight', 'total_weight', 'weight_unit')
    template_name = 'training/workoutset_list.html'
    success_message = 'Edit successfully!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date'].widget = forms.TextInput(attrs={'type': 'date'})
        return form

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


class WorkoutListView(WeekArchiveView, PermissionRequiredMixin, ListView):
    """
    Render list of Workouts objects, set by current logged user
    order by date training id and exercises order.
    Default show current week from Monday to Sunday.
    Verify that the current
    user has all specified permissions.
    """
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
    """
    View for deleting an object retrieved with self.get_object(), with a
    response rendered by a template.
    Add current url of site to context and redirect to
    the previous URL after successfully delete .
    """
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
