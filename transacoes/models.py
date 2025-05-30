from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Transferencia(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transferencias_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transferencias_recebidas')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=10, choices=[('PIX', 'Pix'), ('TED', 'TED'), ('DOC', 'DOC')], default='PIX')
    descricao = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f'{self.remetente.username} → {self.destinatario.username}: R${self.valor}'

class Cartao(models.Model):
    BANDEIRAS = [
        ('VISA', 'Visa'),
        ('MASTERCARD', 'Mastercard'),
        ('ELO', 'Elo'),
        ('AMEX', 'American Express')
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartoes')
    numero = models.CharField(max_length=16)
    bandeira = models.CharField(max_length=20, choices=BANDEIRAS, default='VISA')
    validade = models.DateField()
    cvv = models.CharField(max_length=3)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    limite_disponivel = models.DecimalField(max_digits=10, decimal_places=2)
    dia_vencimento = models.IntegerField(default=10)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Cartão de {self.usuario.username} - Final {self.numero[-4:]}'

class Fatura(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE, related_name='faturas')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=[('ABERTA', 'Aberta'), ('FECHADA', 'Fechada'), ('PAGA', 'Paga')], default='ABERTA')
    data_pagamento = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'Fatura {self.cartao} - Vencimento: {self.data_vencimento}'

class Transacao(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE, related_name='transacoes')
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE, related_name='transacoes', null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(default=timezone.now)
    descricao = models.CharField(max_length=200)
    estabelecimento = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.estabelecimento}: R${self.valor}'

class Investimento(models.Model):
    TIPOS_INVESTIMENTO = [
        ('POUPANCA', 'Poupança'),
        ('CDB', 'CDB'),
        ('TESOURO', 'Tesouro Direto'),
        ('ACOES', 'Ações'),
        ('FUNDOS', 'Fundos de Investimento')
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investimentos')
    tipo = models.CharField(max_length=20, choices=TIPOS_INVESTIMENTO, default='POUPANCA')
    valor_investido = models.DecimalField(max_digits=10, decimal_places=2)
    rendimento = models.DecimalField(max_digits=5, decimal_places=2, help_text='Taxa de rendimento anual em %')
    data_inicio = models.DateField(default=timezone.now)
    data_resgate = models.DateField(null=True, blank=True)
    valor_atual = models.DecimalField(max_digits=10, decimal_places=2)
    valor_resgate = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.get_tipo_display()} - {self.usuario.username} - R${self.valor_investido}'
    
    def calcular_rendimento(self):
        """Calcula o rendimento atual do investimento"""
        if not self.ativo:
            return self.valor_atual
        
        dias_investidos = (timezone.now().date() - self.data_inicio).days
        taxa_diaria = self.rendimento / 365 / 100
        valor_atual = self.valor_investido * (1 + taxa_diaria) ** dias_investidos
        return round(valor_atual, 2)
    
    def atualizar_valor(self):
        """Atualiza o valor atual do investimento"""
        self.valor_atual = self.calcular_rendimento()
        self.valor_resgate = self.valor_atual * 0.9 if self.tipo != 'POUPANCA' else self.valor_atual
        self.save()

class HistoricoInvestimento(models.Model):
    investimento = models.ForeignKey(Investimento, on_delete=models.CASCADE, related_name='historico')
    data = models.DateField(default=timezone.now)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['data']
    
    def __str__(self):
        return f'Histórico {self.investimento} - {self.data}'
