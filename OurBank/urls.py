from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('transacoes/', include('transacoes.urls')),
    path('forum/', include('forum.urls')),
]
