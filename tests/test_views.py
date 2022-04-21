import datetime

import django
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.utils.http import urlencode
from conftest import build_url

import training.models


def test_registration_user(db, client):
    response = client.post(reverse('users:register'), data={
        'username': 'tester123',
        'password1': 'ExamplePass',
        'password2': 'ExamplePass',
    })

    assert response.status_code == 302
    assert get_user_model().objects.all().count() == 1


def test_login_user(created_user, client):
    logged_in = client.login(username='tester', password='ExamplePass')

    assert logged_in


def test_logout_user(created_user, client):
    client.login(username='tester', password='ExamplePass')
    client.logout()

    assert auth.get_user(client).is_anonymous


def test_home_page(client):
    url = reverse('home:home')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Home</h1>' in response.content.decode('utf-8')


def test_login_page(client):
    url = reverse('users:login')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Login</h1>' in response.content.decode('utf-8')


def test_register_page(client):
    url = reverse('users:register')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Register</h1>' in response.content.decode('utf-8')


def test_add_exercise_page_not_logged(client):
    url = reverse('training:create-exercise')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_add_exercise_page_logged(created_user, client):
    client.login(username='tester', password='ExamplePass')
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
    url = reverse('training:create-training')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_add_training_page_logged(created_user, client):
    client.login(username='tester', password='ExamplePass')
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
    url = reverse('training:create-training-plan-name')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_add_training_plan_name_page_logged(created_user, client):
    client.login(username='tester', password='ExamplePass')

    url = reverse('training:create-training-plan-name')
    response = client.get(url)

    assert response.status_code == 200

    response = client.post(reverse('training:create-training-plan-name'), data={
        'training_plan_name': 'Training Plan',
    })
    assert response.status_code == 302
    assert training.models.TrainingPlanName.objects.all().count() == 1


def test_create_training_plan_page_not_logged(client):
    url = reverse('training:create-training-plan')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_create_training_plan_page_logged(created_user, create_plan_name, create_training, create_exercise, client):
    client.login(username='tester', password='ExamplePass')
    url = reverse('training:create-training-plan')
    response = client.get(url)

    assert response.status_code == 200

    response1 = client.post(reverse('training:create-training-plan'), data={
        'training_plan_name': create_plan_name.id,
        'exercise_name': create_exercise.id,
        'order': 1,
        'training': create_training.id,
        'number_of_sets': 3,
        'reps': 10,
        'reps_unit': 'Reps',
        'rest_between_sets': 120,
    })
    assert response1.status_code == 302
    assert training.models.TrainingPlan.objects.all().count() == 1


def test_current_training_plan_page_not_logged(client):
    url = reverse('training:list')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_current_training_plan_page_logged(created_user, create_training_plan, client):
    client.login(username='tester', password='ExamplePass')

    url = reverse('training:list')
    response = client.get(url)

    assert response.status_code == 200

    assert training.models.TrainingPlan.objects.all().count() == 1
    url = build_url('training:list', params={'training_plan_name': 1})
    response = client.get(url)
    assert '<th class="col-3">Training Name: Training</th>' in response.content.decode('utf-8')
    assert response.status_code == 200


def test_add_workout_page_not_logged(client):
    url = reverse('training:workout')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_add_workout_page_logged(created_user, client):
    client.login(username='tester', password='ExamplePass')
    url = reverse('training:workout')
    response = client.get(url)

    assert response.status_code == 200


def test_workout_list_page_not_logged(client):
    url = reverse('training:workout-list', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                   'week': datetime.datetime.now().isocalendar()[1]})
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_workout_list_page_logged(created_user, client):
    client.login(username='tester', password='ExamplePass')
    url = reverse('training:workout-list', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                   'week': datetime.datetime.now().isocalendar()[1]})
    response = client.get(url)

    assert response.status_code == 200


def test_delete_from_training_plane(created_user, client, create_training_plan):
    client.login(username='tester', password='ExamplePass')
    idx = create_training_plan.id

    response = client.post(reverse('training:training_plan-delete', kwargs={'pk': idx}))
    assert response.status_code == 302
