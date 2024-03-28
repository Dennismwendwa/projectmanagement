from django.urls import path
from . import views


app_name = "projects"

urlpatterns = [
     path("dashboard", views.home, name="home"),
     path("", views.landing_page, name="landing_page"),
     path("project/<str:slug>/<str:security_key>", views.project_details,
          name="project_details"),
     path("task-details/<int:pk>", views.task_details, name="task_details"),
     path("completed-task/<int:task_id>", views.task_completed,
          name="task_completed"),
     path('tasks_completed_histogram/<str:slug>/',
          views.tasks_completed_histrogram, name='tasks_completed_histogram'),
     path("subscription", views.package_subscription, name="subscription"),
     path("blogs", views.blog_view, name="blogs"),
     path("blog/<str:slug>", views.blog_details, name="blog_details"),
]