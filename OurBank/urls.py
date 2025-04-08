from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Bem-vindo à Home!</h1>")

urlpatterns = [
    path('', home),  # <- essa linha resolve o erro
    path('forum/', include('forum.urls')),
    path('admin/', admin.site.urls),
]
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('forum/')),
    path('forum/', include('forum.urls')),
    path('admin/', admin.site.urls),
]
