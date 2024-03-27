from functools import wraps
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect
from accounts.models import User, UserSubscription, SubscriptionPlan


def has_access(view_func):
    """
    This function ensure users have access only
    when they have valid plan
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            my_plan = UserSubscription.objects.get(user=request.user)
            if my_plan.end_date > timezone.now():
                    return view_func(request, *args, **kwargs)
        except UserSubscription.DoesNotExist:
            pass
        
        return redirect("projects:landing_page")
    return _wrapped_view