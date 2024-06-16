from django.urls import path, include
from . import views

urlpatterns = [
    path("projects/", views.ProjectView.as_view(), name="projects"),
    path("projects/<int:pk>/", views.ProjectView.as_view(), name="project"),
    path("tasks/", views.TaskView.as_view(), name="tasks"),
    path("tasks/<int:pk>/", views.TaskView.as_view(), name="task"),
    path("tasks/<int:pk>/comments/", views.CommentsView.as_view(), name="comments"),
]
