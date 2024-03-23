from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from .models import BackgroundImage, Project, Task
from .forms import ProjectForm, TaskForm

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
    project.security_key = security_key

    project_tasks = Task.objects.filter(project=project)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            location = form.cleaned_data["location"]
            department = form.cleaned_data["department"]
            description = form.cleaned_data["description"]
            start_date = form.cleaned_data["start_date"]
            deadline = form.cleaned_data["deadline"]

            Task.objects.create(
                project=project,
                name=name,
                location=location,
                department=department,
                description=description,
                start_date=start_date,
                deadline=deadline,
            )
            return redirect("projects:project_details", slug, security_key)
        else:
            print(form.errors)
    form = TaskForm()
    context = {
        "project": project,
        "form": form,
        "project_tasks": project_tasks,
    }
    return render(request, "projects/project_details.html", context)


def task_details(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task_data = model_to_dict(task)
    return JsonResponse(task_data, safe=False)

def landing_page(request):


    return render(request, "projects/landing_page.html")
