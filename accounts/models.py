from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_administrator = models.BooleanField(default=False)


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def can_create_team(self):
        if self.is_administrator:
            return True
        return False


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


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    description = models.TextField()

    class Meta:
        verbose_name = "subscription"
        verbose_name_plural = "subscriptions"
        ordering = ("-pk",)

    def __str__(self):
        return f"Subscription: {self.name} price per month: {self.price}"


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    openning_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class meta:
        verbose_name = "userscription"
        verbose_name_plural = "userscriptions"
        ordering = ("-openning_date",)
    
    def __str__(self):
        return f"Subscription of {self.user.username} plan: {self.plan.name}"
    

class Contact(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"
        ordering = ("-date",)

    def __str__(self):
        return f"{self.full_name} contacted us at {self.date}"