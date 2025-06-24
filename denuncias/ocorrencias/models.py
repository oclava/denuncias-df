from django.db import models
from django.conf import settings

class CategoriaDenuncia(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    descricao = models.TextField(blank=True, verbose_name="Descrição (opcional)")

    class Meta:
        verbose_name = "Categoria de Denúncia"
        verbose_name_plural = "Categorias de Denúncias"
        ordering = ['nome'] 

    def __str__(self):
        return self.nome

class Orgao(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome completo do órgão (ex: Polícia Militar do DF)")
    sigla = models.CharField(max_length=10, unique=True, help_text="Sigla do órgão (ex: PMDF)")
    
    class Meta:
        verbose_name = "Órgão Competente"
        verbose_name_plural = "Órgãos Competentes"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Denuncia(models.Model):
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_analise', 'Em análise'),
        ('encaminhada', 'Encaminhada'),
        ('concluida', 'Concluída'),
        ('rejeitada', 'Rejeitada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    
    localizacao = models.CharField(max_length=400, blank=True, null=True, verbose_name="Endereço da Ocorrência")
    latitude = models.DecimalField(max_digits=30, decimal_places=25, blank=True, null=True)
    longitude = models.DecimalField(max_digits=30, decimal_places=25, blank=True, null=True)
    
    categoria = models.ForeignKey(
        CategoriaDenuncia,
        on_delete=models.PROTECT,
        related_name='denuncias',
        verbose_name="Categoria"
    )
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='aberta')
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    anexo = models.FileField(upload_to='anexos/%Y/%m/%d/', blank=True, null=True)

    orgaos_designados = models.ManyToManyField(
        'Orgao',
        blank=True,
        help_text="Selecione um ou mais órgãos competentes para esta denúncia."
    )

    class Meta:
        verbose_name = "Denúncia"
        verbose_name_plural = "Denúncias"
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo