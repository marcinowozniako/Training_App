import datetime

from django.urls import reverse


def test_login_user(created_user, client):
    logged_in = client.login(username='tester', password='ExamplePass')

    assert logged_in


def test_logout_user(created_user, client):
    client.logout()
    response = client.get('/users/logout')

    assert response.status_code == 302


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


def test_add_exercise_page(created_user, client):
    url = reverse('training:create-exercise')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')

    client.login(username='tester', password='ExamplePass')
    url = reverse('training:create-exercise')
    response = client.get(url)

    assert response.status_code == 200


def test_add_training_page(created_user, client):
    url = reverse('training:create-training')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')

    client.login(username='tester', password='ExamplePass')
    url = reverse('training:create-training')
    response = client.get(url)

    assert response.status_code == 200


def test_add_training_plan_page(created_user, client):
    url = reverse('training:create-training-plan-name')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')

    client.login(username='tester', password='ExamplePass')

    url = reverse('training:create-training-plan-name')
    response = client.get(url)

    assert response.status_code == 200


def test_create_training_plan_page(created_user, client):
    url = reverse('training:create-training-plan')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')

    client.login(username='tester', password='ExamplePass')
    url = reverse('training:create-training-plan')
    response = client.get(url)

    assert response.status_code == 200


def test_current_training_plan_page(created_user, client):
    url = reverse('training:list')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')

    client.login(username='tester', password='ExamplePass')

    url = reverse('training:list')
    response = client.get(url)

    assert response.status_code == 200


def test_add_workout_page(created_user, client):
    url = reverse('training:workout')
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')

    client.login(username='tester', password='ExamplePass')
    url = reverse('training:workout')
    response = client.get(url)

    assert response.status_code == 200


def test_workout_list_page(created_user, client):
    url = reverse('training:workout-list', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                   'week': datetime.datetime.now().isocalendar()[1]})
    response = client.get(url)

    assert response.status_code == 403
    assert '<h1>You need to be logged to view this site!!</h1>' in response.content.decode('utf-8')

    client.login(username='tester', password='ExamplePass')
    url = reverse('training:workout-list', kwargs={'year': datetime.datetime.now().isocalendar()[0],
                                                   'week': datetime.datetime.now().isocalendar()[1]})
    response = client.get(url)

    assert response.status_code == 200
