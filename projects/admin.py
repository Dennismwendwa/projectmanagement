from django.contrib import admin
from .models import Project, BackgroundImage, Task, TaskCompleted, Blog


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "bg_image", "date")
    prepopulated_fields = {"slug": ("name",)}


class TaskAdmin(admin.ModelAdmin):
    list_display = ("project", "name", "location", "department", "start_date",
                    "deadline", "checklist")


class TaskCompletedAdmin(admin.ModelAdmin):
    list_display = ("task", "completed", "completed_date")


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "image", "author", "date")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Project, ProjectAdmin)
admin.site.register(BackgroundImage)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCompleted, TaskCompletedAdmin)
admin.site.register(Blog, BlogAdmin)
