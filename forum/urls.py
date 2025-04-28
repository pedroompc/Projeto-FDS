from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_topicos, name='forum'),
    path('topico/novo/', views.novo_topico, name='novo_topico'),
    path('topico/<int:topico_id>/', views.detalhe_topico, name='detalhe_topico'),
    path('topico/<int:topico_id>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),
]
