from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("add-team-memeber/", views.create_team, name="add_team_member"),
    path("package/", views.select_package, name="select_package"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("contact/", views.contact, name="contact"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("manage-members/", views.delete_team_member, name="manage_members"),
    path("delete-member/<int:pk>/", views.delete_member, name="delete_member"),
]