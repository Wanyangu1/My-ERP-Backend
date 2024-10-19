"""
URL configuration for elearning_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# elearning_platform/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from courses.views import CourseViewSet, ModuleViewSet, ContentViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_nested import routers as nested_routers

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

courses_router = nested_routers.NestedDefaultRouter(router, r'courses', lookup='course')
courses_router.register(r'modules', ModuleViewSet, basename='course-modules')

modules_router = nested_routers.NestedDefaultRouter(courses_router, r'modules', lookup='module')
modules_router.register(r'contents', ContentViewSet, basename='module-contents')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(courses_router.urls)),
    path('api/', include(modules_router.urls)),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
