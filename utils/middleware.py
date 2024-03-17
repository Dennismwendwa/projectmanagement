from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class AdministratorMiddleware:
    """This middleware adds all permissions for models in listed apps"""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_administrator:
            apps_to_grant_permissions = ["accounts", "projects"]

            for app_label in apps_to_grant_permissions:
                app_config = apps.get_app_config(app_label)
                models = app_config.get_models()

                for model in models:
                    content_type = ContentType.objects.get_for_model(model)
                    permissions = Permission.objects.filter(content_type=content_type)
                    
                    for permission in permissions:
                        if permission not in request.user.user_permissions.all():
                            
                            request.user.user_permissions.add(permission)
            return self.get_response(request)
        else:
            return self.get_response(request)