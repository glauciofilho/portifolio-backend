from django.contrib import admin
from .models import Project, Stack, StackProject, File, ProjectAccess


class StackProjectInline(admin.TabularInline):
    model = StackProject
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [StackProjectInline]
    list_display = ("id", "name_pt", "created_at")


@admin.register(Stack)
class StackAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "badge_url")


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "path", "project")


@admin.register(ProjectAccess)
class ProjectAccessAdmin(admin.ModelAdmin):
    list_display = ("project", "ip_address", "country", "accessed_at")
    list_filter = ("project", "country")