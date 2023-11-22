"""
URL configuration for squadsrpint_be project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from main_app import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
router.register(r'groups', views.EmployeeGroupViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'managers', views.ManagerViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'addtask', views.TaskAddViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token-refresh '),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', views.EmployeeRegistration.as_view(), name='employee-registration'),
]
