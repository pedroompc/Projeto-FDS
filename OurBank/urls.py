from django.contrib import admin
from django.urls import path, include
from transacoes import views as transacoes_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', transacoes_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('transacoes/', include('transacoes.urls')),
    path('user/', include('user.urls')),

    # Rotas de autenticação (caso não estejam em user.urls)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]