"""authentication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.views import SignUpViewSet, LoginViewSet, LogoutViewSet
from apps.common.routers import OptionalSlashRouter

router = OptionalSlashRouter()

router.register(r'signup', SignUpViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')

urlpatterns = [
    path('auth/', include(router.urls)),
    path('auth/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
