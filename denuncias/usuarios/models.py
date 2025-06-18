# denuncias/usuarios/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from denuncias.ocorrencias.models import Orgao 

class UsuarioManager(BaseUserManager):
    def create_user(self, cpf, password=None, **extra_fields):
        if not cpf:
            raise ValueError('O CPF é obrigatório.')
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cpf, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # NOVO CAMPO: Adicione date_joined aqui
    date_joined = models.DateTimeField(auto_now_add=True)
    # last_login é fornecido automaticamente por AbstractBaseUser

    orgaos_responsavel = models.ManyToManyField(
        Orgao,
        blank=True, 
        help_text="Órgãos pelos quais este usuário é responsável."
    )

    objects = UsuarioManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome'] 

    def __str__(self):
        return self.cpf

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"