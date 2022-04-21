import pytest
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.http import urlencode

import training
from training import models
from training.apps import TrainingConfig


def build_url(*args, **kwargs):
    params = kwargs.pop('params', {})
    url1 = reverse(*args, **kwargs)
    if params:
        url1 += '?' + urlencode(params)
    return url1


@pytest.fixture
def created_user(db):
    user = User.objects.create(username='tester')
    user.set_password('ExamplePass')
    user.save()
    user1 = User.objects.create(username='tester1')
    user1.set_password('ExamplePass1')
    user1.save()
    group_app, created = Group.objects.get_or_create(name=TrainingConfig.name)

    models_app = apps.all_models[TrainingConfig.name]
    for model in models_app:
        content_type = ContentType.objects.get(
            app_label=TrainingConfig.name,
            model=model
        )
        permissions = Permission.objects.filter(content_type=content_type)
        user.groups.add(group_app)
        user1.groups.add(group_app)
        group_app.permissions.add(*permissions)
    return user


@pytest.fixture
def create_exercise(db):
    exercise = training.models.Exercises.objects.create(name='exercise')
    return exercise


@pytest.fixture
def create_plan_name(created_user, db):
    plan_name = training.models.TrainingPlanName.objects.create(training_plan_name='Training Plan', owner=created_user)
    return plan_name


@pytest.fixture
def create_training(created_user, db):
    training_name = training.models.Training.objects.create(name='Training', owner=created_user)
    return training_name


@pytest.fixture
def create_training_plan(created_user, db, create_training, create_plan_name, create_exercise):
    training_plan = training.models.TrainingPlan.objects.create \
        (training_plan_name=create_plan_name, exercise_name=create_exercise, order=1, training=create_training,
         number_of_sets=3, reps=10, reps_unit='Reps', rest_between_sets=120, owner=created_user)
    return training_plan
