from django.contrib import admin
from .models import Project, BackgroundImage


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "bg_image", "date")
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Project, ProjectAdmin)
admin.site.register(BackgroundImage)
