# courses/views.py
from rest_framework import viewsets, permissions
from .models import Course, Module, Content
from .serializers import CourseSerializer, ModuleSerializer, ContentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        return Module.objects.filter(course__id=course_id, course__teacher=self.request.user)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        serializer.save(course_id=course_id)

class ContentViewSet(viewsets.ModelViewSet):
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        module_id = self.kwargs['module_pk']
        return Content.objects.filter(module__id=module_id, module__course__teacher=self.request.user)

    def perform_create(self, serializer):
        module_id = self.kwargs['module_pk']
        serializer.save(module_id=module_id)
