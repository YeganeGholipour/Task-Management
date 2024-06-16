from django.urls import path, include
from . import views

urlpatterns = [
    path("projects/", views.ProjectView.as_view()),
    path("projects/<int:pk>/", views.ProjectView.as_view()),
    path("tasks/", views.TaskView.as_view()),
    path("tasks/<int:pk>/", views.TaskView.as_view()),
    path("tasks/<int:pk>/comments/", views.CommentsView.as_view()),
]
