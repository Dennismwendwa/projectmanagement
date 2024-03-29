from django.db import models
from accounts.models import User
import random


class Project(models.Model):
    """This models stores all projects data"""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   limit_choices_to={"is_administrator": True},
                                   null=True)
    bg_image = models.ForeignKey("BackgroundImage", on_delete=models.CASCADE,
                                 related_name="project_bg_img")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ("-date",)

    def __str__(self):
        return f"Project name: {self.name}"
    
    @property
    def get_image_url(self):
        return self.bg_image.image.url


class BackgroundImage(models.Model):
    """This class stores projects background images"""
    image = models.ImageField(upload_to="bg_img")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "background image"
        verbose_name_plural = "background images"

    def __str__(self):
        return f"Image: {self.image}"
    
    @classmethod
    def random_image(cls, request):
        """This method selects a random image"""
        images = cls.objects.all()

        selected_image_ids = request.session.get("selected_image_ids", [])
        if selected_image_ids:
            images = images.exclude(id__in=selected_image_ids)

        if len(selected_image_ids) == images.count():
            selected_image_ids = []
            request.session["selected_image_ids"] = selected_image_ids
        
        random_image = random.choice(images)
        selected_image_ids.append(random_image.id)
        request.session["selected_image_ids"] = selected_image_ids
        return random_image if random_image else None

  
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    description = models.TextField()
    workers = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    deadline = models.DateTimeField()
    checklist = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "task"
        verbose_name_plural = "tasks"
        ordering = ("deadline",)
    
    def __str__(self):
        return f"Task name: {self.name} created at {self.created_date}, department: {self.department}"
    

class TaskCompleted(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             limit_choices_to={"checklist": False})
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField()

    class Meta:
        verbose_name = "task completed"
        verbose_name_plural = "tasks completed"

    def __str__(self):
        return f"Task: {self.task.name} completed on {self.completed_date}, dep: {self.task.department}"
