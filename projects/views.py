from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, F
from django.db.models.functions import ExtractMonth
from datetime import datetime
import matplotlib.pyplot as plt
import io
from .models import BackgroundImage, Project, Task, TaskCompleted
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
    current_date = timezone.now()

    histogram_image = tasks_completed_histrogram(request, slug)

    completed_tasks_count = Task.objects.filter(project=project, checklist=True).count()
    uncompleted_tasks_count = Task.objects.filter(project=project, deadline__lt=current_date, checklist=False).count()
    future_tasks_count = Task.objects.filter(project=project, deadline__gte=current_date, checklist=False).count()

    tasks_by_month = Task.objects.filter(project=project).annotate(month=ExtractMonth('deadline')).values('month').annotate(count=Count('id'))
    months = [datetime.strptime(str(month), '%m').strftime('%B') for month in range(1, 13)]
    task_counts = [0] * 12
    for task in tasks_by_month:
        task_counts[task['month'] - 1] = task['count']

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
        "current_date": current_date,
        "completed_tasks_count": completed_tasks_count,
        "uncompleted_tasks_count": uncompleted_tasks_count,
        "future_tasks_count": future_tasks_count,
        "months": months,
        "task_counts": task_counts,
        "histogram_image": histogram_image,
    }
    return render(request, "projects/project_details.html", context)


def task_details(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task_data = model_to_dict(task)
    return JsonResponse(task_data, safe=False)


def task_completed(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    try:
        completed_task = TaskCompleted.objects.get(task=task)
        completed_task.delete()
        task.checklist = False
        task.save()
    except TaskCompleted.DoesNotExist:
        TaskCompleted.objects.create(
            task=task,
            completed=True,
            completed_date=timezone.now()
        )
        task.checklist=True
        task.save()
    return JsonResponse({}
    )


def tasks_completed_histrogram(request, slug):
    project = get_object_or_404(Project, slug=slug)

    tasks_completed_by_department_and_month = TaskCompleted.objects.filter(
        task__project=project).annotate(
        month=ExtractMonth('completed_date'),
        department=F('task__department')).values(
            'department', 'month').annotate(count=Count('id'))

    department_counts_by_month = {}
    for entry in tasks_completed_by_department_and_month:
        department = entry['department']
        month = entry['month']
        count = entry['count']
        if department not in department_counts_by_month:
            department_counts_by_month[department] = [0] * 12
        department_counts_by_month[department][month - 1] = count

    fig, ax = plt.subplots(figsize=(10, 6))
    for department, counts in department_counts_by_month.items():
        ax.bar(range(1, 13), counts, label=department)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([datetime.strptime(str(month), '%m').strftime('%B') for month in range(1, 13)], rotation=45)
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Tasks Completed')
    ax.set_title(f'Tasks Completed by Department and Month for Project: {project.name}')
    ax.legend()
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')


def landing_page(request):

    return render(request, "projects/landing_page.html")
