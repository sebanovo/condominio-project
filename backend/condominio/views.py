from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import Group
from config import settings

from .models import (
    Usuario,
    Casa,
    Vehiculo,
    AreaComun,
    Reserva,
    Multa,
    IngresoSalida,
    Extranjero,
)

from .serializers import (
    UsuarioSerializer,
    CasaSerializer,
    VehiculoSerializer,
    AreaComunSerializer,
    ReservaSerializer,
    MultaSerializer,
    IngresoSalidaSerializer,
    ExtranjeroSerializer,
)

import datetime
from .serializers import UsuarioSerializer
import jwt

"""
#####################################
# AUTENTICACION DE USUARIOS CON JWT #
#####################################
"""


class SignUpView(APIView):
    def post(self, request):
        """Registro de usuario y crear token JWT"""
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        payload = {
            "id": serializer.data["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = serializer.data
        return response


class LoginView(APIView):
    def post(self, request):
        """Login de usuario y crear token JWT"""
        email = request.data["email"]
        password = request.data["password"]

        user = Usuario.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"message": "success"}
        return response


class LogoutView(APIView):
    def post(self, request):
        """
        Eliminar la cookie del token JWT para cerrar sesión
        """
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}
        return response


class UserView(APIView):
    def get(self, request):
        """
        Obtener datas del usuario autenticado
        """
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = Usuario.objects.filter(id=payload["id"]).first()
        serializer = UsuarioSerializer(user)
        return Response(serializer.data)


class ValidateSessionView(APIView):
    def get(self, request):
        """Validar si la sesión (cookie JWT) es válida"""
        token = request.COOKIES.get("jwt")

        if not token:
            return Response(
                {"valid": False, "message": "No hay sesión activa"}, status=401
            )

        try:
            # Decodificar el token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Buscar el usuario
            user = Usuario.objects.filter(id=payload["id"]).first()
            if not user:
                return Response(
                    {"valid": False, "message": "Usuario no encontrado"}, status=401
                )

            # Serializar datos del usuario (sin información sensible)
            user_data = {
                "id": user.id,
                "email": user.email,
                # Agrega otros campos que necesites en el frontend
            }

            return Response({"valid": True, "user": user_data})

        except jwt.ExpiredSignatureError:
            return Response({"valid": False, "message": "Sesión expirada"}, status=401)
        except jwt.InvalidTokenError:
            return Response({"valid": False, "message": "Token inválido"}, status=401)


"""
#####################################################
# METODOS QUE EL ADMIN Y/O EL PERSONAL PUEDEN HACER #
#####################################################
"""


class CasaView(APIView):
    def post(self, request):
        """Crear casa (solo admin y personal, puede hacerlo)"""
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = Usuario.objects.filter(id=payload["id"]).first()
        roles = user.groups.all()

        if (
            not roles.filter(name="Administrador").exists()
            and not roles.filter(name="Personal").exists()
        ):
            raise AuthenticationFailed("You are not admin or personal")

        new_casa = Casa.objects.create(
            nro=request.data["nro"],
            categoria=request.data["categoria"],
            capacidad=request.data["capacidad"],
        )
        new_casa.save()
        return Response({"message": "casa created successfully"})


class AsignarCasaView(APIView):
    def post(self, request):
        """Asignar casa a usuario (solo admin, puede hacerlo)"""
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = Usuario.objects.filter(id=payload["id"]).first()

        if not user.groups.all().filter(name="Administrador").exists():
            raise AuthenticationFailed("You are not admin")

        # asignar casa a usuario no crear la casa
        user_id = request.data["user_id"]
        casa_id = request.data["casa_id"]
        casa = Casa.objects.filter(id=casa_id).first()
        casa.usuarios.add(user_id)
        casa.save()
        return Response({"message": "casa assigned to user successfully"})


class MultaView(APIView):
    def post(self, request):
        """Crear multa (solo admin y personal, puede hacerlo)"""
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = Usuario.objects.filter(id=payload["id"]).first()
        roles = user.groups.all()

        if (
            not roles.filter(name="Administrador").exists()
            and not roles.filter(name="Personal").exists()
        ):
            raise AuthenticationFailed("You are not admin or personal")
        new_multa = Multa.objects.create(
            descripcion=request.data["descripcion"],
            monto=request.data["monto"],
            fecha=request.data["fecha"],
            estado_pago=request.data["estado_pago"],
            id_usuario=Usuario.objects.filter(id=request.data["id_usuario"]).first(),
        )
        new_multa.save()
        return Response({"message": "multa created successfully"})


class IngresoSalidaView(APIView):
    def post(self, request):
        """Crear ingreso/salida a usuario (solo Administrador y Personal, puede hacerlo)"""
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = Usuario.objects.filter(id=payload["id"]).first()

        roles = user.groups.all()
        if (
            not roles.filter(name="Administrador").exists()
            and not roles.filter(name="Personal").exists()
        ):
            raise AuthenticationFailed("You are not admin or personal")

        persona_id = request.data["persona_id"]

        # crear un ingreso salida
        new_ingreso_salida = IngresoSalida.objects.create(
            fecha=request.data["fecha"],
            tipo=request.data["tipo"],
            modo=request.data["modo"],
            es_extranjero=request.data["es_extranjero"],
        )

        if request.data["es_extranjero"]:
            new_ingreso_salida.extranjero_id = Extranjero.objects.filter(
                id=persona_id
            ).first()
        else:
            new_ingreso_salida.id_usuario_id = Usuario.objects.filter(
                id=persona_id
            ).first()
        new_ingreso_salida.save()
        return Response({"message": "ingreso/salida assigned to persona successfully"})


class VehiculoView(APIView):
    def post(self, request):
        """Crear vehiculo (solo admin y personal, puede hacerlo)"""
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        roles = Usuario.objects.filter(id=payload["id"]).first().groups.all()
        if (
            not roles.filter(name="Administrador").exists()
            and not roles.filter(name="Personal").exists()
        ):
            raise AuthenticationFailed("You are not admin or personal")

        new_vehiculo = Vehiculo.objects.create(
            placa=request.data["placa"],
            tipo=request.data["tipo"],
            color=request.data["color"],
            id_usuario=Usuario.objects.filter(id=request.data["id_usuario"]).first(),
        )
        new_vehiculo.save()
        return Response({"message": "vehiculo created successfully"})


class ReservaView(APIView):
    def post(self, request):
        """Asignar reserva a usuario (solo Admin y Personal, puede hacerlo)"""
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = Usuario.objects.filter(id=payload["id"]).first()

        roles = user.groups.all()
        if (
            not roles.filter(name="Administrador").exists()
            and roles.filter(name="Personal").exists()
        ):
            raise AuthenticationFailed("You are not admin or personal")

        user_id = request.data["id_usuario"]
        reserva_id = request.data["id_area"]
        new_reserva = Reserva.objects.create(
            fecha=request.data["fecha"],
            estado_pago=request.data["estado_pago"],
            metodo_pago=request.data["metodo_pago"],
            id_area=AreaComun.objects.filter(id=reserva_id).first(),
            id_usuario=Usuario.objects.filter(id=user_id).first(),
        )
        new_reserva.save()
        return Response({"message": "reserva assigned to user successfully"})


class AreaComunView(APIView):
    def post(self, request):
        """Crear area comun (solo Admin y Personal, puede hacerlo)"""
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = Usuario.objects.filter(id=payload["id"]).first()

        roles = user.groups.all()
        if (
            not roles.filter(name="Administrador").exists()
            and not roles.filter(name="Personal").exists()
        ):
            raise AuthenticationFailed("You are not admin or personal")

        new_area = AreaComun.objects.create(
            nombre=request.data["nombre"],
            descripcion=request.data["descripcion"],
            horario=request.data["horario"],
            costo=request.data["costo"],
        )
        new_area.save()
        return Response({"message": "area comun created successfully"})


class ExtranjeroView(APIView):
    def post(self, request):
        """Crear extranjero (solo admin y personal, puede hacerlo)"""
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        roles = Usuario.objects.filter(id=payload["id"]).first().groups.all()
        if (
            not roles.filter(name="Administrador").exists()
            and not roles.filter(name="Personal").exists()
        ):
            raise AuthenticationFailed("You are not admin or personal")

        new_extranjero = Extranjero.objects.create(
            ci=request.data["ci"],
            nombre=request.data["nombre"],
        )
        new_extranjero.save()
        return Response({"message": "extranjero created successfully"})


"""
#####################################
# METODOS PARA LISTAR LOS REGISTROS #
#####################################
"""


class CasasListView(APIView):
    def get(self, request):
        """Ver casas del residente autenticado"""
        casas = Casa.objects.all()
        serializer = CasaSerializer(casas, many=True)
        token = request.COOKIES.get("jwt")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = Usuario.objects.filter(id=payload["id"]).first()
        serializer = CasaSerializer(user.casas, many=True)
        return Response(serializer.data)


class MultasListView(APIView):
    def get(self, request):
        """Ver multas del residente autenticado"""
        multas = Multa.objects.all()
        serializer = MultaSerializer(multas, many=True)
        token = request.COOKIES.get("jwt")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = Usuario.objects.filter(id=payload["id"]).first()
        multa = Multa.objects.filter(id_usuario=user)
        serializer = MultaSerializer(multa, many=True)
        return Response(serializer.data)


class VehiculosListView(APIView):
    def get(self, request):
        """Ver vehiculos del residente autenticado"""
        vehiculos = Vehiculo.objects.all()
        serializer = VehiculoSerializer(vehiculos, many=True)
        token = request.COOKIES.get("jwt")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = Usuario.objects.filter(id=payload["id"]).first()
        vehiculo = Vehiculo.objects.filter(id_usuario=user)
        serializer = VehiculoSerializer(vehiculo, many=True)
        return Response(serializer.data)


class ReservasListView(APIView):
    def get(self, request):
        """Ver reservas del residente autenticado"""
        reservas = Reserva.objects.all()
        serializer = ReservaSerializer(reservas, many=True)
        token = request.COOKIES.get("jwt")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = Usuario.objects.filter(id=payload["id"]).first()
        reserva = Reserva.objects.filter(id_usuario=user)
        serializer = ReservaSerializer(reserva, many=True)
        return Response(serializer.data)


class AreasComunesListView(APIView):
    def get(self, request):
        """Ver areas comunes"""
        areas = AreaComun.objects.all()
        serializer = AreaComunSerializer(areas, many=True)
        return Response(serializer.data)


# METODO PARA LISTAR TODO
class UsuariosAllView(ListAPIView):
    queryset = Usuario.objects.filter()
    serializer_class = UsuarioSerializer


class ResidentesAllView(ListCreateAPIView):
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        role_group = Group.objects.get(name="Residente")
        return Usuario.objects.filter(groups=role_group)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Guardar el nuevo usuario
        self.perform_create(serializer)

        # Asignar grupo "Residente"
        residente_group = Group.objects.get(name="Residente")
        usuario = serializer.instance
        usuario.groups.add(residente_group)

        headers = self.get_success_headers(serializer.data)
        return Response({"message": "succes"})


# admin
# asignar casa a usuario ✔
# asignar multa a usuario ✔

# admin y personal
# asignar ingreso/salida a usuario ✔
# asignar vehiculo a usuario ✔
# asignar reserva a usuario ✔

# residente
# ver sus casas ✔
# ver sus multas ✔
# ver sus vehiculos ✔
# ver sus ingresos/salidas ✔
# ver sus reservas ✔
# ver areas comunes ✔
