from django import forms
from .models import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ["created_by", "bg_image", "date"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["created_date", "project", "workers", "checklist"]