from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=450)
    nota_geral = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)

    def __str__(self):
        return self.nome

    def calcular_nota_geral(self):
        avaliacoes = Avaliacao.objects.filter(empresa=self)
        if avaliacoes.exists():
            media = avaliacoes.aggregate(models.Avg('nota'))['nota__avg']
            self.nota_geral = round(media, 2)
            self.save()

class Avaliacao(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='avaliacoes', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comentario = models.TextField()

    def __str__(self):
        return f'Avaliação para {self.empresa.nome} por {self.usuario.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.empresa.calcular_nota_geral()
