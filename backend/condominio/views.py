from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

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


class SignUpView(APIView):
    def post(self, request):
        print("Entro Aqui")
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        payload = {
            "id": serializer.data["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = serializer.data
        return response


class LoginView(APIView):
    def post(self, request):
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

        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"message": "success"}
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = Usuario.objects.filter(id=payload["id"]).first()
        serializer = UsuarioSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}
        return response


class CasaView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = Usuario.objects.filter(id=payload["id"]).first()
        serializer = UsuarioSerializer(user)
        return Response(serializer.data)


# class CasaListCreateView(ListCreateAPIView):
#     # queryset = Casa.objects.all()
#     # serializer_class = CasaSerializer
#     # permission_classes = [IsAuthenticated]


class CasaListCreateView(APIView):
    # obtener las casas del usuario autenticado
    def get(self, request):
        casas = Casa.objects.all()
        serializer = CasaSerializer(casas, many=True)
        token = request.COOKIES.get("jwt")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = Usuario.objects.filter(id=payload["id"]).first()
        serializer = CasaSerializer(user.casas, many=True)
        return Response(serializer.data)

    # Asignar casa a usuario (solo admin, puede hacerlo)
    def post(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = Usuario.objects.filter(id=payload["id"]).first()
        if not user.is_superuser:
            raise AuthenticationFailed("You are not admin")
        # asignar casa a usuario no crear la casa
        user_id = request.data["user_id"]
        casa_id = request.data["casa_id"]
        casa = Casa.objects.filter(id=casa_id).first()
        casa.usuarios.add(user_id)
        casa.save()
        return Response({"message": "casa assigned to user successfully"})

    # def put(self, request, pk):
    #     casa = Casa.objects.get(pk=pk)
    #     serializer = CasaSerializer(casa, data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)

    #     return Response(serializer.errors, status=400)
