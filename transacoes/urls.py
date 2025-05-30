from django.urls import path
from . import views

urlpatterns = [
    path('transferencias/', views.transferencias, name='transferencias'),
    path('transferencia/nova/', views.nova_transferencia, name='nova_transferencia'),
    path('transferencia/<int:transferencia_id>/', views.detalhe_transferencia, name='detalhe_transferencia'),
    path('cartoes/', views.cartoes, name='cartoes'),
    path('cartao/novo/', views.adicionar_cartao, name='adicionar_cartao'),  # Nova rota adicionada
    path('cartao/<int:cartao_id>/', views.detalhe_cartao, name='detalhe_cartao'),
    path('faturas/', views.faturas, name='faturas'),
    path('fatura/<int:fatura_id>/', views.detalhe_fatura, name='detalhe_fatura'),
    path('investimentos/', views.investimentos, name='investimentos'),
    path('investimento/novo/', views.novo_investimento, name='novo_investimento'),
    path('investimento/<int:investimento_id>/', views.detalhe_investimento, name='detalhe_investimento'),
]
