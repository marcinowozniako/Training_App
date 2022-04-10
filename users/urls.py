from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.registration_view, name='register'),

]
