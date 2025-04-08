from django.contrib import admin
from django.urls import path, include
from transacoes import views as transacoes_views

urlpatterns = [
    path('', transacoes_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('transacoes/', include('transacoes.urls')),
]
