from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pix/', views.transferencia_pix, name='transferencia_pix'),
]
