from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Profile, Contact, SubscriptionPlan, UserSubscription


class UserAdmin(UA):
    list_display = ('username', 'email', "first_name", "last_name",
                    'is_staff', 'is_administrator')
    search_fields = ('username', 'email')
    ordering = ('username',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "date")


class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discount")


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "openning_date", "start_date", "end_date")


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Contact, ContactAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
