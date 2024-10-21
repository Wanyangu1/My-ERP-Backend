# courses/serializers.py
from rest_framework import serializers
from .models import Course, Module, Content
from django.contrib.auth.models import User
from django.contrib.auth.models import User  # or your custom User model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Add other fields you want to expose


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = '__all__'

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description']

class CourseListSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()  

    class Meta:
        model = Course
        fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):
    courses = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'courses']
