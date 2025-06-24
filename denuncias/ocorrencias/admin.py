from django.contrib import admin
from .models import CategoriaDenuncia, Denuncia, Orgao

@admin.register(CategoriaDenuncia)
class CategoriaDenunciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao') 
    search_fields = ('nome',) 


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'status', 'data_criacao')
    list_filter = ('status', 'categoria', 'orgaos_designados')
    search_fields = ('titulo', 'descricao')

    fieldsets = (
        (None, {'fields': ('titulo', 'descricao', 'categoria', 'status')}),
        ('Localização e Anexos', {'fields': ('localizacao', 'anexo')}),
        ('Atribuição', {'fields': ('orgaos_designados',)}),
        ('Informações do Sistema', {'fields': ('usuario', 'data_criacao', 'ultima_atualizacao')}), 
    )
    readonly_fields = ('usuario', 'data_criacao', 'ultima_atualizacao')


@admin.register(Orgao)
class OrgaoAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome')
    search_fields = ('sigla', 'nome')