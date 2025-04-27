from django.db import models

class Topico(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='topicos')
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-data_criacao']

class Comentario(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='comentarios')
    
    def __str__(self):
        return f'Comentário de {self.autor.username} em {self.topico.titulo}'
    
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['data_criacao']
