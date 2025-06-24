from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario 
from denuncias.ocorrencias.models import Orgao 

@admin.register(Usuario) 
class UsuarioAdmin(BaseUserAdmin):
    list_display = ('cpf', 'nome', 'is_staff', 'is_active', 'get_orgaos_responsavel')
    list_filter = ('is_staff', 'is_active', 'orgaos_responsavel')
    search_fields = ('cpf', 'nome',)
    
    ordering = ('cpf',) 

    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        ('Informações Pessoais', {'fields': ('nome',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
        ('Designação de Órgãos', {'fields': ('orgaos_responsavel',)}),
    )
    readonly_fields = ('last_login', 'date_joined')

    def get_orgaos_responsavel(self, obj):
        return ", ".join([orgao.sigla for orgao in obj.orgaos_responsavel.all()])
    get_orgaos_responsavel.short_description = 'Órgãos Responsáveis'