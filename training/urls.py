from django.urls import path

from . import views

app_name = 'training'

urlpatterns = [
    path('create-exercise', views.CreateExerciseView.as_view(), name='create-exercise'),
    path('create-training', views.CreateTrainingView.as_view(), name='create-training'),

]
