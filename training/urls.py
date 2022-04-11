from django.urls import path

from . import views

app_name = 'training'

urlpatterns = [
    path('create-exercise', views.CreateExerciseView.as_view(), name='create-exercise'),
    path('create-training', views.CreateTrainingView.as_view(), name='create-training'),
    path('create-training-plan', views.CreateTrainingPlanView.as_view(), name='create-training-plan'),
    path('list', views.ListTrainingPlanView.as_view(), name='list'),
    path('detail/<pk>', views.DetailExerciseView.as_view(), name='exercise-detail'),
    path('new_workout', views.WorkoutView.as_view(), name='workout'),
    path('workout/list', views.WorkoutListView.as_view(), name='workout-list'),
    path('workout/list/edit/<pk>', views.WorkoutUpdateView.as_view(), name='workout-edit'),

]
