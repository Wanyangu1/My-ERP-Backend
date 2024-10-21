# courses/views.py
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from .models import Course, Module, Content
from .serializers import CourseListSerializer, ModuleSerializer, ContentSerializer, CourseCreateSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "User created successfully"})
    
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)



class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Ensure user is logged in

    def get_queryset(self):
        # Only show courses created by the logged-in teacher
        return Course.objects.filter(teacher=self.request.user)

    def get_serializer_class(self):
        # Dynamically switch between serializers based on the action
        if self.action in ['list', 'retrieve']:  # List and detail views
            return CourseListSerializer
        return CourseCreateSerializer  # For creating a course

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the teacher
        serializer.save(teacher=self.request.user)

class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated] 
    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        return Module.objects.filter(course__id=course_id, course__teacher=self.request.user)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        serializer.save(course_id=course_id)

    @action(detail=True, methods=['get'], url_path='modules', url_name='module_list')
    def list_modules(self, request, course_pk=None):
        """
        List all modules for a specific course.
        """
        course = self.get_object()
        modules = Module.objects.filter(course=course)
        serializer = self.get_serializer(modules, many=True)
        return Response(serializer.data)

class ContentViewSet(viewsets.ModelViewSet):
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]   

    def get_queryset(self):
        module_id = self.kwargs['module_pk']
        return Content.objects.filter(module__id=module_id, module__course__teacher=self.request.user)

    def perform_create(self, serializer):
        module_id = self.kwargs['module_pk']
        serializer.save(module_id=module_id)
