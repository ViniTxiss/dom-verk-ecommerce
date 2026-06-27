from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'buyer_name', 'buyer_email', 'buyer_phone', 'buyer_cpf',
            'address_zip', 'address_street', 'address_number',
            'address_complement', 'address_neighborhood',
            'address_city', 'address_state', 'payment_method', 'notes',
        ]
        widgets = {
            'buyer_name': forms.TextInput(attrs={'placeholder': 'Seu nome completo', 'class': 'form-input'}),
            'buyer_email': forms.EmailInput(attrs={'placeholder': 'seu@email.com', 'class': 'form-input'}),
            'buyer_phone': forms.TextInput(attrs={'placeholder': '(11) 99999-9999', 'class': 'form-input'}),
            'buyer_cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00', 'class': 'form-input'}),
            'address_zip': forms.TextInput(attrs={'placeholder': '00000-000', 'class': 'form-input', 'id': 'cep'}),
            'address_street': forms.TextInput(attrs={'placeholder': 'Rua, Avenida...', 'class': 'form-input'}),
            'address_number': forms.TextInput(attrs={'placeholder': 'Nº', 'class': 'form-input'}),
            'address_complement': forms.TextInput(attrs={'placeholder': 'Apto, Bloco... (opcional)', 'class': 'form-input'}),
            'address_neighborhood': forms.TextInput(attrs={'placeholder': 'Bairro', 'class': 'form-input'}),
            'address_city': forms.TextInput(attrs={'placeholder': 'Cidade', 'class': 'form-input'}),
            'address_state': forms.TextInput(attrs={'placeholder': 'UF', 'class': 'form-input', 'maxlength': '2'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'payment-radio'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Alguma observação? (opcional)', 'class': 'form-input', 'rows': 3}),
        }
        labels = {
            'buyer_name': 'Nome Completo',
            'buyer_email': 'E-mail',
            'buyer_phone': 'Telefone',
            'buyer_cpf': 'CPF',
            'address_zip': 'CEP',
            'address_street': 'Endereço',
            'address_number': 'Número',
            'address_complement': 'Complemento',
            'address_neighborhood': 'Bairro',
            'address_city': 'Cidade',
            'address_state': 'Estado',
            'payment_method': 'Forma de Pagamento',
            'notes': 'Observações',
        }
