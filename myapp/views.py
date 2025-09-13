from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(response):
    return HttpResponse("<h1>Hola home</h1>")

def about(response):
    return HttpResponse("<h1>Hola about</h1>")