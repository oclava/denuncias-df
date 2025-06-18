from django import forms
from .models import Denuncia

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['titulo', 'descricao', 'categoria', 'localizacao', 'anexo']
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
                'placeholder': 'Ex: Rua das Flores, Quadra 10, Lote 5, Taguatinga-DF',
                'maxlength': '255',
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
            'localizacao': 'Localização (opcional)',
            'anexo': 'Anexar Prova (opcional)'
        }
        help_texts = {
            'localizacao': 'Se souber, informe o endereço exato ou ponto de referência.',
            'anexo': 'Formatos aceitos: JPG, PNG, PDF, MP4 (até 5MB)'
        }

class AdminDenunciaAssignmentForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        # AQUI ESTÁ A MUDANÇA: Use 'orgaos_designados' em vez de 'orgao_competente'
        fields = ['status', 'orgaos_designados'] 
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'orgaos_designados': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
