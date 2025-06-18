from django.contrib import admin
from .models import CategoriaDenuncia, Denuncia, Orgao

@admin.register(CategoriaDenuncia)
class CategoriaDenunciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao') # Campos para exibir na lista do admin
    search_fields = ('nome',) # Campos para pesquisa

# Registra o modelo denuncia
@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'status', 'data_criacao')
    list_filter = ('status', 'categoria', 'orgaos_designados')
    search_fields = ('titulo', 'descricao')

    fieldsets = (
        (None, {'fields': ('titulo', 'descricao', 'categoria', 'status')}),
        ('Localização e Anexos', {'fields': ('localizacao', 'anexo')}),
        ('Atribuição', {'fields': ('orgaos_designados',)}),
        ('Informações do Sistema', {'fields': ('usuario', 'data_criacao', 'ultima_atualizacao')}), # Adicionado para exibir campos automáticos
    )
    # Define campos que não devem ser editáveis no admin
    readonly_fields = ('usuario', 'data_criacao', 'ultima_atualizacao')


# Registra o modelo Orgao
@admin.register(Orgao)
class OrgaoAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome')
    search_fields = ('sigla', 'nome')