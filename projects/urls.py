from django.urls import path
from . import views


app_name = "projects"

urlpatterns = [
    path("dashboard", views.home, name="home"),
    path("", views.landing_page, name="landing_page"),
    path("project/<str:slug>/<str:security_key>", views.project_details,
         name="project_details"),
    path("task-details/<int:pk>", views.task_details, name="task_details"),
]