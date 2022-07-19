from django.urls import path

from . import views

app_name = 'training'

urlpatterns = [
    path('create-exercise', views.CreateExerciseView.as_view(), name='create-exercise'),
    path('create-training', views.CreateTrainingView.as_view(), name='create-training'),
    path('create-training-plan-name', views.CreateTrainingPlanNameView.as_view(), name='create-training-plan-name'),
    path('create-training-plan', views.CreateTrainingPlanView.as_view(), name='create-training-plan'),
    path('list', views.ListTrainingPlanView.as_view(), name='list'),
    path('detail/<pk>', views.DetailExerciseView.as_view(), name='exercise-detail'),
    path('new_workout', views.AddWorkoutView.as_view(), name='workout'),
    path('workout/list/<year>/<week>', views.WorkoutListView.as_view(), name='workout-list'),
    path('workout/list/<year>/<week>/edit/<pk>', views.WorkoutUpdateView.as_view(), name='workout-edit'),
    path('detail/edit/<pk>', views.UpdateExerciseView.as_view(), name='exercise-edit'),
    path('list/edit/<pk>', views.TrainingPlanUpdateView.as_view(), name='training_plan-edit'),
    path('list/delete/<pk>', views.DeleteTrainingPlanView.as_view(), name='training_plan-delete'),
    path('workout/list/<year>/<week>/delete/<pk>', views.DeleteExerciseWorkoutView.as_view(), name='workout_ex-delete'),
    path('list/delete/plan/<pk>', views.DeleteTrainingPlanNameView.as_view(), name='training_plan_name-delete'),
    path('ajax/load-filtered_training/', views.load_training_for_selected_training_plan, name='ajax_load_training'),
]
