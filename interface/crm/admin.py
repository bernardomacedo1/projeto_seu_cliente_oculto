from django.contrib import admin
from .models import Empresa, Avaliacao

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome', 'descricao']

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'usuario', 'nota', 'comentario']
    search_fields = ['empresa__nome', 'usuario__username', 'nota', 'comentario']
