from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, Group
from django.utils import timezone
from datetime import timedelta
from .models import User, SubscriptionPlan, UserSubscription
from .forms import ContactForm


def register(request):
    """This view registers new users"""
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        role = request.POST.get("role", "")
        is_administrator = request.POST.get("is_administrator", True)
        subscription_plan = request.POST.get("subscription_plan")
        
        if password1 == password2 and len(password1) > 7:
            if User.objects.filter(username=username).exists():
                messages.warning(request, f"Username already taken")
                return redirect("accounts:register")
            elif User.objects.filter(email=email).exists():
                messages.warning(request, f"Email already in use")
                return redirect("accounts:register")
            else:
                user = User.objects.create_user(username=username,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                password=password1,)
                start_date=timezone.now()
                if subscription_plan == "free":
                    plan = SubscriptionPlan.objects.get(name="Free Plan")
                elif subscription_plan == "business":
                    plan = SubscriptionPlan.objects.get(name="Business Plan")
                elif subscription_plan == "developer":
                    plan = SubscriptionPlan.objects.get(name="Developer Plan")
                UserSubscription.objects.create(
                    user=user,
                    plan=plan,
                    start_date=start_date,
                    end_date=start_date + timedelta(days=30)
                )
                
                if is_administrator:
                    user.is_administrator = True
                    user.save()
                if role:
                    try:
                        role = role.capitalize()
                        group = Group.objects.get(name=role)
                    except Group.DoesNotExist:
                        group = Group.objects.create(name=role)
                    group.user_set.add(user)

                status = login_helper(request, username, password1)
                if status == "success":
                    return redirect("projects:home")

        elif len(password1) < 8:
            messages.warning(request, f"Password MUST have minimum of 8 characters!")
            return redirect("accounts:register")
        else:
            messages.warning(request, "Password not matching")
            return redirect("accounts:register")
    return render(request, "accounts/register.html", {"admin_user": True})

def create_team(request):
    if request.method == "POST":
        
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        role = request.POST.get("role", "member")
        team_member = request.POST["team_member"]

        subscription_plan = UserSubscription.objects.get(user=request.user)

        if password1 == password2 and len(password1) > 7:
            if User.objects.filter(username=username).exists():
                messages.warning(request, f"Username already taken")
                return redirect("accounts:register")
            elif User.objects.filter(email=email).exists():
                messages.warning(request, f"Email already in use")
                return redirect("accounts:register")
            else:
                user = User.objects.create_user(username=username,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                password=password1,)
                start_date=timezone.now()

                UserSubscription.objects.create(
                    user=user,
                    plan=subscription_plan.plan,
                    user_admin=request.user,
                    start_date=subscription_plan.start_date,
                    end_date=subscription_plan.end_date
                )
                
                user.team_member = True
                user.save()
                if role:
                    try:
                        role = role.capitalize()
                        group = Group.objects.get(name=role)
                    except Group.DoesNotExist:
                        group = Group.objects.create(name=role)
                    group.user_set.add(user)

                status = login_helper(request, username, password1)
                if status == "success":
                    return redirect("projects:home")
    return render(request, "accounts/register.html")

def select_package(request):
    return render(request, "accounts/package_selection.html")


def login_helper(request, username, password):
    """Helper function for login users"""
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return "success"
    else:
        messages.warning(request, f"Invalid username or password")
        return redirect("accounts:login")


def login(request):
    """This view is for login users"""

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if not username or not password:
            messages.warning(request, "Please enter both username and password")
            return redirect("accounts:login")
        
        status = login_helper(request, username, password)
        if status == "success":
            return redirect("projects:home")
    
    return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    return redirect("projects:landing_page")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your message has been sent. Thank you!")
            return redirect("accounts:contact")
        else:
            print(form.errors)
    return render(request, "accounts/contact.html")

def aboutus(request):
    return render(request, "accounts/aboutus.html")
