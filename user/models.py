from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_conta = models.CharField(max_length=10, choices=[('PESSOAL', 'Pessoal'), ('EMPRESA', 'Empresa')], default='PESSOAL')
    
    def __str__(self):
        return f'Perfil de {self.usuario.username}'
