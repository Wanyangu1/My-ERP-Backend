# courses/models.py
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.course.title})"

class Content(models.Model):
    CONTENT_TYPES = (
        ('text', 'Text'),
        ('file', 'File'),
        ('video', 'Video URL'),
        ('image', 'Image'),
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='content_files/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='content_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_type} in {self.module.title}"
