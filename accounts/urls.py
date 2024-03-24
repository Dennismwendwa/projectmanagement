from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("contact/", views.contact, name="contact"),
    path("aboutus/", views.aboutus, name="aboutus")
]