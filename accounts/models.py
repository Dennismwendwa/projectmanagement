from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(default="default.jpg",
                                        upload_to='profile_pictures/')
    country = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"


    def __str__(self):
        return f"Profile of {self.user.username}. Created at {self.date_joined}"