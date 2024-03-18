from django.shortcuts import render, redirect, get_object_or_404
from .models import BackgroundImage, Project
from .forms import ProjectForm

import uuid


def home(request):
    projects = Project.objects.all()
    security_key = uuid.uuid4()

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_name = form.cleaned_data["name"]
            image = BackgroundImage.random_image(request)
            Project.objects.create(
                name=project_name,
                created_by=request.user,
                bg_image=image,
            )
            return redirect("projects:home")
        else:
            print(form.errors)
    for project in projects:
        project.security_key = uuid.uuid4()
    context = {
        "projects": projects,
    }
    return render(request, "projects/home.html", context)


def project_details(request, slug, security_key):
    project = get_object_or_404(Project, slug=slug)
    
    context = {
        "project": project,    
    }
    return render(request, "projects/project_details.html", context)

def landing_page(request):


    return render(request, "projects/landing_page.html")
