from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import PerfilSerializer, CasaSerializer, UserSignupSerializer
from .models import Perfil, Casa
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import generics
from django.contrib.auth.models import User


# Create your views here.
def home(response):
    return HttpResponse("<h1>Hola home</h1>")


class PerfilView(viewsets.ModelViewSet):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()


# @api_view(["GET", "POST"])
# def listar(request):
#     if request.method == "GET":
#         casas = Casa.objects.all()
#         response = CasaSerializer(casas, many=True)
#         return Response(response.data)
#     elif request.method == "POST":
#         response = CasaSerializer(data=request.data)
#         if response.is_valid():
#             response.save()
#             return Response(response.data, status=status.HTTP_200_OK)
#         return Response(response._errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
