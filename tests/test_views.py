import datetime
import time

import pytest
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.urls import reverse

import training.models
from conftest import build_url


@pytest.mark.parametrize('username, password1, password2, status_code, number', (
        ('tester', 'ExamplePass', 'ExamplePass', 302, 1),
        ('', 'ExamplePass', 'ExamplePass', 200, 0),
        ('a', 'ExamplePass4', 'ExamplePass4', 200, 0),
        ('tester1', 'ExamplePass1', 'ExamplePass1', 302, 1),
        ('tester', 'password', 'password', 200, 0),
        ('tester2', 'ExamplePass1', 'ExamplePass', 200, 0),
        ('tester', 'ExamplePass', 'ExamplePass2', 200, 0),
        ('tester4', '', 'ExamplePass2', 200, 0),
        ('tester4', 'ExamplePass2', '', 200, 0),
        ('tester4', '', '', 200, 0),
        ('', '', '', 200, 0),
))
def test_registration_user(db, client, username, password1, password2, status_code, number):
    """
    Test of registration form view with multiple data
    """
    response = client.post(reverse('users:register'), data={
        'username': username,
        'password1': password1,
        'password2': password2,
    })

    assert response.status_code == status_code
    assert get_user_model().objects.all().count() == number


def test_login_user(created_user, client):
    """Test of login user"""
    response = client.post(reverse('users:login'), data={
        'username': created_user.username,
        'password': 'ExamplePass',
    })
    assert response.status_code == 302


def test_logout_user(created_user, client, log_in_user):
    """Test of logout user"""
    response = client.post(reverse('users:logout'))
    assert response.status_code == 302
    assert auth.get_user(client).is_anonymous


def test_home_page(client):
    """Test to check if home page working"""
    url = reverse('home:home')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Home</h1>' in response.content.decode('utf-8')


def test_login_page(client):
    """Test to check if login page working"""
    url = reverse('users:login')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Login</h1>' in response.content.decode('utf-8')


def test_register_page(client):
    """Test to check if register page working"""
    url = reverse('users:register')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Register</h1>' in response.content.decode('utf-8')


def test_add_exercise_page_not_logged(client):
    """Test to check if add_exercise page requires permissions to see """
    url = reverse('training:create-exercise')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_add_exercise_page_logged(client, log_in_user):
    """Test to check if logged User can add new exercise by form on page"""
    url = reverse('training:create-exercise')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Add new Exercise</h1>' in response.content.decode('utf-8')

    response = client.post(reverse('training:create-exercise'), data={
        'name': 'exercise',
    })

    assert response.status_code == 302
    assert training.models.Exercises.objects.all().count() == 1


def test_add_training_page_not_logged(client):
    """Test to check if add_training page requires permissions to see """
    url = reverse('training:create-training')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_add_training_page_logged(log_in_user, client):
    """Test to check if logged User can add new training by form on page"""
    url = reverse('training:create-training')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Add new Training</h1>' in response.content.decode('utf-8')

    response = client.post(reverse('training:create-training'), data={
        'name': 'Training',
    })

    assert response.status_code == 302
    assert training.models.Training.objects.all().count() == 1


def test_add_training_plan_name_page_not_logged(client):
    """Test to check if add_training_plan_name page requires permissions to see """
    url = reverse('training:create-training-plan-name')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_add_training_plan_name_page_logged(log_in_user, client):
    """Test to check if logged User can add new training plan name by form on page"""
    url = reverse('training:create-training-plan-name')
    response = client.get(url)

    assert response.status_code == 200

    response = client.post(reverse('training:create-training-plan-name'), data={
        'training_plan_name': 'Training Plan',
    })
    assert response.status_code == 302
    assert training.models.TrainingPlanName.objects.all().count() == 1


def test_create_training_plan_page_not_logged(client):
    """Test to check if create_training_plan page requires permissions to see """
    url = reverse('training:create-training-plan')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_create_training_plan_page_logged(log_in_user, create_plan_name, create_training, create_exercise, client):
    """Test to check if logged User can create new training plan by form on page"""
    url = reverse('training:create-training-plan')
    response = client.get(url)

    assert response.status_code == 200

    response = client.post(reverse('training:create-training-plan'), data={
        'training_plan_name': create_plan_name.id,
        'exercise_name': create_exercise.id,
        'order': 1,
        'training': create_training.id,
        'number_of_sets': 3,
        'reps': 10,
        'reps_unit': 'Reps',
        'rest_between_sets': 120,
    })
    assert response.status_code == 302
    assert training.models.TrainingPlan.objects.all().count() == 1


def test_current_training_plan_page_not_logged(client):
    """Test to check if current_training_plan page requires permissions to see """
    url = reverse('training:list')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_current_training_plan_page_logged(log_in_user, create_training_plan, client):
    """Test to check if logged User can see current training plan on page"""
    url = reverse('training:list')
    response = client.get(url)

    assert response.status_code == 200

    assert training.models.TrainingPlan.objects.all().count() == 1
    url = build_url('training:list', params={'training_plan_name': 1})
    response = client.get(url)
    assert '<th class="col-3">Training Name: Training</th>' in response.content.decode('utf-8')
    assert response.status_code == 200


def test_add_workout_page_not_logged(client):
    """Test to check if add_workout page requires permissions to see """
    url = reverse('training:workout')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_add_workout_page_logged(log_in_user, client, create_exercise, create_day):
    """Test to check if logged User can add new workout by form on page"""
    url = reverse('training:workout')
    response = client.get(url)

    assert response.status_code == 200

    response = client.post(reverse('training:workout'), data={
        'date': time.strftime("%Y-%m-%d"),
        'day': create_day.id,
        'exercise': create_exercise.id,
        'sets': 3,
        'reps': 10,
        'reps_unit': 'Reps',
        'weight_unit': 'Kg',
    })
    assert response.status_code == 302


def test_workout_list_page_not_logged(client):
    """Test to check if workout_list page requires permissions to see """
    url = reverse('training:workout-list', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                   'week': datetime.datetime.now().isocalendar()[1]})
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_workout_list_page_logged(log_in_user, client, create_workout):
    """Test to check if logged User can see added workout on page"""
    url = reverse('training:workout-list', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                   'week': datetime.datetime.now().isocalendar()[1]})
    response = client.get(url)

    assert response.status_code == 200
    assert '<td class="col-3">exercise</td>' in response.content.decode('utf-8')


def test_detail_exercise_page_logged(create_exercise, client, log_in_user):
    """Test to check if logged User can see details of exercise on page"""
    idx = create_exercise.id
    url = reverse('training:exercise-detail', kwargs={'pk': idx})
    response = client.get(url)

    assert response.status_code == 200
    assert '<th scope="row" class="col-2">Name of Exercise</th>' in response.content.decode('utf-8')


def test_delete_from_training_plane(log_in_user, client, create_training_plan):
    """Test to check if logged User can delete exercise from training plan"""
    idx = create_training_plan.id

    response = client.post(reverse('training:training_plan-delete', kwargs={'pk': idx}))
    assert response.status_code == 302
    assert training.models.TrainingPlan.objects.all().count() == 0


def test_edit_training_plan_logged(log_in_user, create_training_plan, client):
    """Test to check if logged User can edit exercise from training plan"""
    idx = create_training_plan.id
    assert training.models.TrainingPlan.objects.all().count() == 1

    response_post = client.post(reverse('training:training_plan-edit', kwargs={'pk': idx}), data={
        'training_plan_name': create_training_plan.training_plan_name.id,
        'exercise_name': create_training_plan.exercise_name.id,
        'order': 1,
        'training': create_training_plan.training.id,
        'number_of_sets': 4,
        'reps': 10,
        'reps_unit': 'Reps',
        'rest_between_sets': 120,
    })

    assert response_post.status_code == 302
    assert str(training.models.TrainingPlan.objects.values('number_of_sets')) == "<QuerySet [{'number_of_sets': 4}]>"


def test_edit_exercise_logged(create_exercise, client, log_in_user):
    """Test to check if logged User can edit exercise"""
    idx = create_exercise.id

    response = client.post(reverse('training:exercise-edit', kwargs={'pk': idx}), data={
        'name': 'new_exercise'

    })

    assert response.status_code == 302
    assert str(training.models.Exercises.objects.values('name')) == "<QuerySet [{'name': 'new_exercise'}]>"


def test_delete_from_workout_list(log_in_user, client, create_workout):
    """Test to check if logged User can delete exercise from workout list"""
    idx = create_workout.id

    response = client.post(
        reverse('training:workout_ex-delete', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                      'week': datetime.datetime.now().isocalendar()[1], 'pk': idx}))
    assert response.status_code == 302
    assert training.models.WorkoutSet.objects.all().count() == 0


def test_edit_workout_object(log_in_user, client, create_workout, create_day, create_exercise):
    """Test to check if logged User can edit exercise from workout list"""
    idx = create_workout.id

    response = client.post(
        reverse('training:workout-edit', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                 'week': datetime.datetime.now().isocalendar()[1], 'pk': idx}), data={
            'date': time.strftime("%Y-%m-%d"),
            'day': create_day.id,
            'exercise': create_exercise.id,
            'sets': 4,
            'reps': 10,
            'reps_unit': 'Reps',
            'weight_unit': 'Kg',
        })
    assert response.status_code == 302
    assert str(training.models.WorkoutSet.objects.values('sets')) == "<QuerySet [{'sets': 4}]>"
