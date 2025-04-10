from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Transferencia(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transferencias_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transferencias_recebidas')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.remetente} → {self.destinatario}: R${self.valor}'

