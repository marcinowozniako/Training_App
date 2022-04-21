import datetime
import time

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.urls import reverse

import training.models
from conftest import build_url


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


def test_add_workout_page_logged(created_user, client, create_exercise, create_day):
    client.login(username='tester', password='ExamplePass')
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
    url = reverse('training:workout-list', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                   'week': datetime.datetime.now().isocalendar()[1]})
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')


def test_workout_list_page_logged(created_user, client, create_workout):
    client.login(username='tester', password='ExamplePass')
    url = reverse('training:workout-list', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                   'week': datetime.datetime.now().isocalendar()[1]})
    response = client.get(url)

    assert response.status_code == 200
    assert '<td class="col-3">exercise</td>' in response.content.decode('utf-8')


def test_detail_exercise_page_logged(create_exercise, client):
    client.login(username='tester', password='ExamplePass')
    idx = create_exercise.id
    url = reverse('training:exercise-detail', kwargs={'pk': idx})
    response = client.get(url)

    assert response.status_code == 200
    assert '<th scope="row" class="col-2">Name of Exercise</th>' in response.content.decode('utf-8')


def test_delete_from_training_plane(created_user, client, create_training_plan):
    client.login(username='tester', password='ExamplePass')
    idx = create_training_plan.id

    response = client.post(reverse('training:training_plan-delete', kwargs={'pk': idx}))
    assert response.status_code == 302


def test_edit_training_plan_logged(created_user, create_training_plan, client):
    client.login(username='tester', password='ExamplePass')
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


def test_edit_exercise_logged(create_exercise, client, created_user):
    client.login(username='tester', password='ExamplePass')
    idx = create_exercise.id

    response = client.post(reverse('training:exercise-edit', kwargs={'pk': idx}), data={
        'name': 'new_exercise'

    })

    assert response.status_code == 302
    assert str(training.models.Exercises.objects.values('name')) == "<QuerySet [{'name': 'new_exercise'}]>"


def test_delete_from_workout_list(created_user, client, create_workout):
    client.login(username='tester', password='ExamplePass')
    idx = create_workout.id

    response = client.post(
        reverse('training:workout_ex-delete', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                      'week': datetime.datetime.now().isocalendar()[1], 'pk': idx}))
    assert response.status_code == 302


def test_edit_workout_object(created_user, client, create_workout, create_day, create_exercise):
    client.login(username='tester', password='ExamplePass')
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
