import time

import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.http import urlencode

import training
from training import models
from training.apps import TrainingConfig


def build_url(*args, **kwargs):
    """Custom function for ability to add get param in reverse function """
    params = kwargs.pop('params', {})
    url1 = reverse(*args, **kwargs)
    if params:
        url1 += '?' + urlencode(params)
    return url1


@pytest.fixture
def created_user(db):
    """Fixture for created user with all permissions"""
    user = get_user_model().objects.create(username='tester')
    user.set_password('ExamplePass')
    user.save()
    group_app, created = Group.objects.get_or_create(name=TrainingConfig.name)

    models_app = apps.all_models[TrainingConfig.name]
    for model in models_app:
        content_type = ContentType.objects.get(
            app_label=TrainingConfig.name,
            model=model
        )
        permissions = Permission.objects.filter(content_type=content_type)
        user.groups.add(group_app)
        group_app.permissions.add(*permissions)
    return user


@pytest.fixture
def log_in_user(db, client, created_user):
    """Fixture for all tests of views with required permissions"""
    login_in = client.login(username='tester', password='ExamplePass')
    return login_in


@pytest.fixture
def create_exercise(db):
    """Fixture for all tests with required exercise to be created"""
    exercise = training.models.Exercises.objects.create(name='exercise')
    return exercise


@pytest.fixture
def create_plan_name(created_user, db):
    """Fixture for all tests with required training plan name to be created"""
    plan_name = training.models.TrainingPlanName.objects.create(training_plan_name='Training Plan', owner=created_user)
    return plan_name


@pytest.fixture
def create_training(created_user, db):
    """Fixture for all tests with required training to be created"""
    training_name = training.models.Training.objects.create(name='Training', owner=created_user)
    return training_name


@pytest.fixture
def create_training_plan(created_user, db, create_training, create_plan_name, create_exercise):
    """Fixture for all tests with required training plan to be created"""
    training_plan = training.models.TrainingPlan.objects.create \
        (training_plan_name=create_plan_name, exercise_name=create_exercise, order=1, training=create_training,
         number_of_sets=3, reps=10, reps_unit='Reps', rest_between_sets=120, owner=created_user)
    return training_plan


@pytest.fixture
def create_day():
    """Fixture for all tests with required day to be created"""
    days = training.models.DayName.objects.create(day_name=0, order=1)
    return days


@pytest.fixture
def create_workout(created_user, create_exercise, create_day):
    """Fixture for all tests with required workout to be created"""
    workout = training.models.WorkoutSet.objects.create \
        (date=time.strftime("%Y-%m-%d"), day=create_day, exercise=create_exercise, sets=3, reps=10, reps_unit='Reps',
         weight_unit='Kg', owner=created_user)
    return workout
