from django import forms
from .models import Usuario 
from django.forms.widgets import PasswordInput

class UsuarioCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha",
        widget=PasswordInput(attrs={
            'placeholder': '********', 
            'minlength': '6', 
            'class': 'form-control'
        }),
        strip=False, #removendo espaços em branco
        min_length=6,
        help_text="A senha deve ter no mínimo 6 caracteres."
    )
    
    confirm_password = forms.CharField(
        label="Confirmar Senha",
        widget=PasswordInput(attrs={ #oculta a senha no front
            'placeholder': '********', 
            'class': 'form-control'
        }),
        strip=False
    )

    class Meta:
        model = Usuario
        fields = ('cpf', 'nome',)
        widgets = {
            'cpf': forms.TextInput(attrs={
                'placeholder': '12312312312', 
                'pattern': r'\d{11}', 
                'class': 'form-control'
            }),
            'nome': forms.TextInput(attrs={
                'placeholder': 'Seu nome completo', 
                'class': 'form-control'
            }),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Usuario.objects.filter(cpf=cpf).exists(): #impede de duplicar usuarios no banco
            raise forms.ValidationError("Este CPF já está cadastrado.")
        if not cpf.isdigit() or len(cpf) != 11: #valida o formato
            raise forms.ValidationError("O CPF deve conter exatamente 11 dígitos numéricos.")
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.") 
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False) 
        user.set_password(self.cleaned_data["password"])
        user.is_active = True  
        user.is_staff = False  

        if commit: 
            user.save()
        return user