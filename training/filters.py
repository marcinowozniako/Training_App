# import django_filters
from django_filters import FilterSet, ModelChoiceFilter

from training import models


def owner(request):
    return models.TrainingPlanName.objects.filter(owner=request.user)


class SnippetFilter(FilterSet):
    training_plan_name = ModelChoiceFilter(queryset=owner)

    class Meta:
        model = models.TrainingPlanName
        fields = ['training_plan_name']
