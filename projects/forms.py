from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ["created_by", "bg_image", "date"]