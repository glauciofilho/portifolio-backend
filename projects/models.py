from django.db import models


class Project(models.Model):
    name_pt = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)

    summary_pt = models.TextField()
    summary_en = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_pt


class Stack(models.Model):
    name = models.CharField(max_length=100, unique=True)
    badge_url = models.URLField()

    def __str__(self):
        return self.name


class StackProject(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="stack_links"
    )
    stack = models.ForeignKey(
        Stack,
        on_delete=models.CASCADE,
        related_name="project_links"
    )

    class Meta:
        unique_together = ("project", "stack")

    def __str__(self):
        return f"{self.project} - {self.stack}"


class File(models.Model):
    project = models.ForeignKey(
        Project,
        related_name="files",
        on_delete=models.CASCADE
    )

    path = models.CharField(
        max_length=255,
        help_text="Ex: src/components/Button"
    )

    content_pt = models.TextField()
    content_en = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.path


class ProjectAccess(models.Model):
    project = models.ForeignKey(
        Project,
        related_name="accesses",
        on_delete=models.CASCADE
    )

    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=100, blank=True)
    user_agent = models.TextField(blank=True)
    accessed_at = models.DateTimeField(auto_now_add=True)