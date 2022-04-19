import django_filters


from training import models


def owner(request):
    return models.TrainingPlanName.objects.filter(owner=request.user)


class SnippetFilter(django_filters.FilterSet):
    training_plan_name = django_filters.ModelChoiceFilter(queryset=owner)

    class Meta:
        model = models.TrainingPlanName
        fields = ['training_plan_name']
