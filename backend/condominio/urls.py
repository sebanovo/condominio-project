from django.urls import path
from .views import (
    # autenticacion de usuario
    SignUpView,
    LoginView,
    LogoutView,
    UserView,
    # admin y/o personal
    CasaView,
    AsignarCasaView,
    AsignarMultaView,
    IngresoSalidaView,
    VehiculoView,
    AsignarVehiculoView,
    ReservaView,
    AreaComunView,
    ExtranjeroView,
    # residente
    CasasListView,
    MultasListView,
    VehiculosListView,
    ReservasListView,
    AreasComunesListView,
)


urlpatterns = [
    # autenticacion de usuario
    path("v1/signup/", SignUpView.as_view(), name="signup"),
    path("v1/login/", LoginView.as_view(), name="login"),
    path("v1/logout/", LogoutView.as_view(), name="logout"),
    path("v1/user/", UserView.as_view(), name="user"),
    # admin y/o personal
    path("v1/casa/", CasaView.as_view(), name="casa"),
    path("v1/asignar-casa/", AsignarCasaView.as_view(), name="asignar-casa"),
    path("v1/asignar-multa/", AsignarMultaView.as_view(), name="asignar-multa"),
    path("v1/ingreso-salida/", IngresoSalidaView.as_view(), name="ingreso-salida"),
    path("v1/vehiculo/", VehiculoView.as_view(), name="vehiculo"),
    path(
        "v1/asignar-vehiculo/", AsignarVehiculoView.as_view(), name="asignar-vehiculo"
    ),
    path("v1/reserva/", ReservaView.as_view(), name="reserva"),
    path("v1/area-comun/", AreaComunView.as_view(), name="area-comun"),
    path("v1/extranjero/", ExtranjeroView.as_view(), name="extranjero"),
    # residente
    path("v1/casas/", CasasListView.as_view(), name="casas"),
    path("v1/multas/", MultasListView.as_view(), name="multas"),
    path("v1/vehiculos/", VehiculosListView.as_view(), name="vehiculos"),
    path("v1/reservas/", ReservasListView.as_view(), name="reservas"),
    path("v1/areas-comunes/", AreasComunesListView.as_view(), name="areas-comunes"),
]
