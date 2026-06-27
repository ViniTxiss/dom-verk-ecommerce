from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com', 'class': 'form-input'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-input'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Sobrenome', 'class': 'form-input'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nome de usuário', 'class': 'form-input'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuário ou e-mail', 'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-input'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address_zip', 'address_street', 'address_number',
            'address_complement', 'address_neighborhood',
            'address_city', 'address_state',
        ]
        widgets = {f: forms.TextInput(attrs={'class': 'form-input'}) for f in [
            'first_name', 'last_name', 'phone',
            'address_zip', 'address_street', 'address_number',
            'address_complement', 'address_neighborhood',
            'address_city', 'address_state',
        ]}
