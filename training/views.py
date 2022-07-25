from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
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
    fields = ('name', 'description', 'training_plan_name')
    template_name = 'training/create_training.html'
    permission_required = 'training.add_training'
    success_url = reverse_lazy('training:create-training')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['training_plan_name'].queryset = models.TrainingPlanName.objects.filter(owner=self.request.user)
        return form


class CreateTrainingPlanNameView(BaseCreateView):
    """
    View for creating a new training plan object, with a response rendered by a template.
    Verify that the current user has all specified permissions.
    If the form is valid, add the current logged user as owner and redirect to the supplied URL.
    """
    model = models.TrainingPlanName
    fields = ('training_plan_name',)
    permission_required = 'training.add_trainingplanname'
    success_url = reverse_lazy('training:create-training-plan-name')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def load_training_for_selected_training_plan(request):
    training_plan_name_id = request.GET.get('training_plan_name')
    training_filtered = models.Training.objects.filter(training_plan_name_id=training_plan_name_id)
    return render(request, 'training_dropdown.html', {'training_filtered': training_filtered})


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

    # def form_invalid(self, form, **kwargs):
    #     training_id = int(self.request.POST.get('training_plan_name'))
    #     form.fields['training'].queryset = models.Training.objects.filter(
    #         training_plan_name_id=training_id)
    #     # ctx = self.get_context_data(**kwargs)
    #     # form.fields['training'].queryset = models.Training.objects.none()
    #     # form.instance.training = self.request.POST.get('training_plan_name')
    #     # form.data = form.data.copy()
    #     # form.data['training'] = models.Training.objects.filter(
    #     #     training_plan_name_id=training_id)
    #     # ctx['form'] = form
    #     # return self.render_to_response(ctx)
    #
    #     if 'training_plan_name' in self.request.POST:
    #
    #
    #
    #     # except (ValueError, TypeError):
    #     #         pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     # else:
    #     #     form.fields['training'].queryset = models.Training.objects.none()
    #
    #     return super().form_invalid(form)

    def get_form(self, form_class=None):
        url = reverse_lazy('training:create-training')
        url1 = reverse_lazy('training:create-training-plan-name')
        url3 = reverse_lazy('training:create-exercise')
        form = super().get_form(form_class=None)
        # form.fields['training'] = forms.ChoiceField(disabled=True)
        # form.fields['training'].queryset = models.Training.objects.none()

        # elif form.instance.pk:
        #     form.fields['training'].queryset = form.instance.country.city_set.order_by('name')

        if form.fields['exercise_name'].queryset.all().count() >= 1:
            form.fields['exercise_name'].queryset = form.fields['exercise_name'].queryset.all()
        else:
            form.fields['exercise_name'] = forms.ChoiceField(help_text=mark_safe(
                f"<a href='{url3}'> You Need to Add Exercise First!</a>"), disabled=True)
        if form.fields['training'].queryset.filter(owner=self.request.user).count() >= 1:
            form.fields['training'].queryset = form.fields['training'].queryset.filter(
                 owner=self.request.user)
        # else:
        #     form.fields['training'] = forms.ChoiceField(help_text=mark_safe(
        #         f"<a href='{url}'> You Need to Add Training First!</a>"), disabled=True)
        if form.fields['training_plan_name'].queryset.filter(
                owner=self.request.user).count() >= 1:
            form.fields['training_plan_name'].queryset = form.fields['training_plan_name'].queryset.filter(
                owner=self.request.user)
        else:
            form.fields['training_plan_name'] = forms.ChoiceField(help_text=mark_safe(
                f"<a href='{url1}'> You Need to Add Training Plan Name First!</a>"), disabled=True)
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


class TrainingPlanUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
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
    permission_required = 'training.change_trainingplan'
    raise_exception = True

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            ctx['id'] = self.request.META['HTTP_REFERER']
        except KeyError:
            ctx['id'] = reverse_lazy('home:home')
        return ctx

    def get_success_url(self):
        try:
            self.success_url = self.request.POST.get('next')
            return self.success_url.format(**self.object.__dict__)
        except AttributeError:
            return reverse_lazy('home:home')


class DeleteTrainingPlanView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """
    View for deleting an object retrieved with self.get_object(), with a
    response rendered by a template.
    """
    model = models.TrainingPlan
    success_url = reverse_lazy('training:list')
    success_message = 'Delete successfully!'
    permission_required = 'training.delete_trainingplan'
    raise_exception = True


class DetailExerciseView(PermissionRequiredMixin, DetailView):
    """
    Render a "detail" view of an object.
    """
    model = models.Exercises
    permission_required = 'training.view_exercises'
    raise_exception = True


class UpdateExerciseView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """
    View for updating an object, with a response rendered by a template.
    Add current url of site to context and redirect to
    the previous URL after successfully edit .
    """

    model = models.Exercises
    fields = '__all__'
    success_message = 'Edit successfully!'
    permission_required = 'training.change_exercises'
    raise_exception = True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            ctx['id'] = self.request.META['HTTP_REFERER']
        except KeyError:
            ctx['id'] = reverse_lazy('home:home')
        return ctx

    def get_success_url(self):
        try:
            self.success_url = self.request.POST.get('next')
            return self.success_url.format(**self.object.__dict__)
        except AttributeError:
            return reverse_lazy('home:home')


class AddWorkoutView(BaseCreateView):
    """
    View for creating a new workout object, with a response rendered by a template.
    Verify that the current user has all specified permissions.
    Change the type of field date for date.
    If the form is valid, add the current logged user as owner and redirect to the supplied URL.
    """

    # def get_queryset(self):
    #     return None

    model = models.WorkoutSet
    fields = ('date', 'day', 'exercise', 'sets', 'reps', 'reps_unit', 'weight', 'total_weight', 'weight_unit',
              'training_plan_name')
    template_name = 'training/workout.html'
    permission_required = 'training.add_workoutset'
    success_url = reverse_lazy('training:workout')

    def get_form(self, form_class=None):
        url = reverse_lazy('training:create-exercise')
        form = super().get_form(form_class)
        if form.fields['exercise'].queryset.all().count() >= 1:
            form.fields['exercise'].queryset = form.fields['exercise'].queryset.all()
        else:
            form.fields['exercise'] = forms.ChoiceField(help_text=mark_safe(
                f"<a href='{url}'> You Need to Add Exercise First!</a>"), disabled=True)
        form.fields['date'].widget = forms.TextInput(attrs={'type': 'date'})
        form.fields['training_plan_name'].queryset = models.TrainingPlanName.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class WorkoutUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """
    View for updating an object, with a response rendered by a template.
    Change the type of field date for date.
    If the form is valid, add the current logged user as owner.
    Add current url of site to context and redirect to
    the previous URL after successfully edit .
    """
    model = models.WorkoutSet
    fields = ('date', 'day', 'exercise', 'sets', 'reps', 'reps_unit', 'weight', 'total_weight', 'weight_unit',
              'training_plan_name')
    template_name = 'training/workoutset_list.html'
    success_message = 'Edit successfully!'
    permission_required = 'training.change_workoutset'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date'].widget = forms.TextInput(attrs={'type': 'date'})
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            ctx['id'] = self.request.META['HTTP_REFERER']
        except KeyError:
            ctx['id'] = reverse_lazy('home:home')
        return ctx

    def get_success_url(self):
        try:
            self.success_url = self.request.POST.get('next')
            return self.success_url.format(**self.object.__dict__)
        except AttributeError:
            return reverse_lazy('home:home')

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
        # for e in data:
        #     if e.exercise not in new_data:
        #         new_data[e.exercise] = [e]
        #     else:
        #         new_data[e.exercise].append(e)
        if self.request.GET.get('training_plan_name') != '':
            qs = self.model.objects.filter(
                training_plan_name=self.request.GET.get('training_plan_name'),
                owner=self.request.user)
            return qs
        else:
            return self.model.objects.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['choose'] = filters.SnippetFilter(self.request.GET, request=self.request, queryset=self.get_queryset())
        return ctx

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     ctx = super().get_context_data()
    #     selected = self.request.GET.getlist('')

    model = models.WorkoutSet
    permission_required = 'training.view_workoutset'
    raise_exception = True
    template_name = 'training/workoutset_list.html'
    week_format = '%W'
    date_field = 'date'
    allow_future = True
    allow_empty = True


class DeleteExerciseWorkoutView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """
    View for deleting an object retrieved with self.get_object(), with a
    response rendered by a template.
    Add current url of site to context and redirect to
    the previous URL after successfully delete .
    """
    model = models.WorkoutSet
    success_message = 'Delete successfully!'
    template_name = 'training/trainingplan_confirm_delete.html'
    permission_required = 'training.delete_workoutset'
    raise_exception = True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            ctx['id'] = self.request.META['HTTP_REFERER']
        except KeyError:
            ctx['id'] = reverse_lazy('home:home')
        return ctx

    def get_success_url(self):
        try:
            self.success_url = self.request.POST.get('next')
            return self.success_url.format(**self.object.__dict__)
        except AttributeError:
            return reverse_lazy('home:home')


class DeleteTrainingPlanNameView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """
    View for deleting an object retrieved with self.get_object(), with a
    response rendered by a template.
    Add current url of site to context and redirect to
    the previous URL after successfully delete .
    """
    model = models.TrainingPlanName
    success_message = 'Delete successfully!'
    template_name = 'training/trainingplan_confirm_delete.html'
    permission_required = 'training.delete_trainingplanname'
    raise_exception = True
    success_url = reverse_lazy('training:list')
