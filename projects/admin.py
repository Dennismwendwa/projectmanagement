from django.contrib import admin
from .models import Project, BackgroundImage, Task, TaskCompleted


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "bg_image", "date")
    prepopulated_fields = {"slug": ("name",)}


class TaskAdmin(admin.ModelAdmin):
    list_display = ("project", "name", "location", "department", "start_date",
                    "deadline", "checklist")


class TaskCompletedAdmin(admin.ModelAdmin):
    list_display = ("task", "completed", "completed_date")


admin.site.register(Project, ProjectAdmin)
admin.site.register(BackgroundImage)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCompleted, TaskCompletedAdmin)
