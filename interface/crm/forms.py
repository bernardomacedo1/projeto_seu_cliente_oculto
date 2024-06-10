from django import forms
from .models import Empresa, Avaliacao
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class CriarUsuario(UserCreationForm):
    username = forms.CharField(
        label='Nome de usuário',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
        error_messages={
            'required': 'Este campo é obrigatório.',
            'unique': 'Um usuário com este nome já existe.',
        }
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Insira um endereço de email válido.',
        }
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        error_messages={
            'required': 'Este campo é obrigatório.',
        }
    )
    password2 = forms.CharField(
        label='Confirme a senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'}),
        error_messages={
            'required': 'Este campo é obrigatório.',
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def _post_clean(self):
        super()._post_clean()
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                validate_password(password1, self.instance)
            except ValidationError as error:
                # Translate built-in password validation errors
                error_messages = {
                    'password_too_short': 'Esta senha é muito curta. Deve conter pelo menos 8 caracteres.',
                    'password_too_common': 'Esta senha é muito comum.',
                    'password_entirely_numeric': 'Esta senha é inteiramente numérica.',
                    'password_too_similar': 'Sua senha é muito similar a suas outras informações pessoais.',
                }
                for e in error.error_list:
                    if e.code in error_messages:
                        e.message = error_messages[e.code]
                self.add_error('password1', error)

class LogarUsuario(AuthenticationForm):
    username = forms.CharField(
        label='Nome de usuário',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
        error_messages={
            'required': 'Este campo é obrigatório.',
        }
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        error_messages={
            'required': 'Este campo é obrigatório.',
        }
    )

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'descricao', 'nota_geral']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da empresa'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição da empresa'}),
            'nota_geral': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nota geral (0-10)', 'readonly': True}),
        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        widgets = {
            'nota': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nota (0-10)', 'min': 0, 'max': 10, 'step': 1}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comentário'}),
        }

    def clean_nota(self):
        nota = self.cleaned_data.get('nota')
        if not isinstance(nota, int) or nota < 0 or nota > 10:
            raise forms.ValidationError("A nota deve ser um número inteiro entre 0 e 10.")
        return nota
