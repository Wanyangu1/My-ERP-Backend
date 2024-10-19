from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('courses/', views.CourseListView.as_view(), name='course_list'),  # List all courses
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),  # View course details, including modules
    path('courses/<int:course_pk>/modules/<int:module_pk>/', views.ModuleDetailView.as_view(), name='module_detail'),  # View module details, including content
]
