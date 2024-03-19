from django.contrib import admin
from .models import Project, BackgroundImage, Task


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "bg_image", "date")
    prepopulated_fields = {"slug": ("name",)}


class TaskAdmin(admin.ModelAdmin):
    list_display = ("project", "name", "location", "department", "start_date",
                    "deadline", "checklist")


admin.site.register(Project, ProjectAdmin)
admin.site.register(BackgroundImage)
admin.site.register(Task, TaskAdmin)
