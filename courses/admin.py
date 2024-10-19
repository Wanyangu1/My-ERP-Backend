from django.contrib import admin
from .models import Course, Module, Content

# Inline for managing modules within a course
class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1  # Allows adding one extra module

# Inline for managing content within a module
class ContentInline(admin.TabularInline):
    model = Content
    extra = 1  # Allows adding one extra content item

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')  # Fields to display in the course list view
    list_filter = ('teacher', 'created_at')  # Filter options for courses
    search_fields = ('title', 'teacher__username')  # Search bar in admin
    inlines = [ModuleInline]  # Include the ModuleInline to manage modules in the course admin

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')  # Fields to display in the module list view
    list_filter = ('course',)  # Filter options for modules
    search_fields = ('title',)  # Search bar in admin
    inlines = [ContentInline]  # Include the ContentInline to manage content in the module admin

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'module', 'created_at')  # Fields to display in the content list view
    list_filter = ('content_type',)  # Filter options for content
    search_fields = ('module__title',)  # Search by module title
