from django.urls import path, include
from . import views
from .views import RegisterView, login_view
from rest_framework.routers import DefaultRouter
from . import views
from .views import LogoutView
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

app_name = 'courses'

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'), 
    path('courses/<int:course_pk>/modules/', views.ModuleListView.as_view(), name='module_list'), 
    path('courses/<int:course_pk>/modules/<int:module_pk>/', views.ModuleDetailView.as_view(), name='module_detail'),  
]
