from django.urls import path
from .views import SignUpView, LoginView, UserView, LogoutView
from .views import (
    CasaView,
    CasaListCreateView,
    # VehiculoView,
    # AreaComunView,
    # ReservaView,
    # MultaView,
    # IngresoSalidaView,
    # ExtranjeroView,
)

urlpatterns = [
    # usuario
    path("v1/signup/", SignUpView.as_view(), name="signup"),
    path("v1/login/", LoginView.as_view(), name="login"),
    path("v1/logout/", LogoutView.as_view(), name="logout"),
    path("v1/user/", UserView.as_view(), name="user"),
    # casa
    path("v1/casas/", CasaListCreateView.as_view(), name="casa"),
]
