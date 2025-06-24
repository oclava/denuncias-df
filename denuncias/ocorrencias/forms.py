from django import forms
from .models import Denuncia

from django import forms
from .models import Denuncia, Orgao, CategoriaDenuncia

class DenunciaForm(forms.ModelForm):
    latitude = forms.DecimalField(max_digits=30, decimal_places=25, required=False, widget=forms.HiddenInput())
    longitude = forms.DecimalField(max_digits=30, decimal_places=25, required=False, widget=forms.HiddenInput())

    class Meta:
        model = Denuncia
        fields = ['titulo', 'descricao', 'categoria', 'localizacao', 'latitude', 'longitude', 'anexo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Buraco na rua X',
                'maxlength': '100',
                'required': True
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descreva a situação com o máximo de detalhes possível.',
                'required': True
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'localizacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Será preenchido automaticamente ao clicar no mapa ou digite aqui.',
                'maxlength': '400',
                'blank': True 
            }),
            'anexo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,video/*,application/pdf',
                'blank': True
            }),
        }
        labels = {
            'titulo': 'Título da Denúncia*',
            'descricao': 'Descrição Detalhada*',
            'categoria': 'Categoria*',
            'localizacao': 'Localização da Ocorrência',
            'anexo': 'Anexar Prova (opcional)'
        }
        help_texts = {
            'localizacao': 'Clique no mapa para definir a localização exata ou digite o endereço.',
            'anexo': 'Formatos aceitos: JPG, PNG, PDF, MP4 (até 5MB)'
        }


class AdminDenunciaAssignmentForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['status', 'orgaos_designados'] 
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'orgaos_designados': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
