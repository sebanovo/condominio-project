from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register(r"perfil", views.PerfilView, "perfil")


# example: http://localhost:8000/mysite/api/v1/perfil/
urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/docs/", include_docs_urls(title="Condominio API")),
    #
    path("api/v1/signup/", views.SignupView.as_view(), name="signup"),
    path("api/v1/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/v1/refresh/", TokenRefreshView.as_view(), name="refresh"),
    # path("auth/signup/", views.SignupAPIView.as_view(), name="signup"),
    # path("auth/login/", views.LoginAPIView.as_view(), name="login"),
    # path("auth/logout/", views.LogoutAPIView.as_view(), name="logout"),
    # path("auth/profile/", views.UserProfileAPIView.as_view(), name="profile"),
]
