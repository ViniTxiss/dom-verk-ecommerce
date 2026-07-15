from django import forms
from apps.orders.models import Coupon


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            'code', 'discount_type', 'discount_value',
            'min_purchase_value', 'valid_from', 'valid_until',
            'max_uses', 'active',
        ]
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'EX: CUPOM10', 'class': 'form-input', 'style': 'text-transform: uppercase;'}),
            'discount_type': forms.Select(attrs={'class': 'form-input'}),
            'discount_value': forms.NumberInput(attrs={'placeholder': '10.00', 'class': 'form-input', 'step': '0.01'}),
            'min_purchase_value': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-input', 'step': '0.01'}),
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}, format='%Y-%m-%dT%H:%M'),
            'valid_until': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}, format='%Y-%m-%dT%H:%M'),
            'max_uses': forms.NumberInput(attrs={'placeholder': 'Sem limite', 'class': 'form-input'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        labels = {
            'code': 'Código do Cupom',
            'discount_type': 'Tipo de Desconto',
            'discount_value': 'Valor do Desconto',
            'min_purchase_value': 'Valor Mínimo de Compra (R$)',
            'valid_from': 'Válido a Partir de',
            'valid_until': 'Válido Até',
            'max_uses': 'Limite Máximo de Usos',
            'active': 'Cupom Ativo',
        }
        help_texts = {
            'code': 'Exemplo: DOM10. Será convertido automaticamente para maiúsculas.',
            'discount_value': 'Para porcentagem, digite ex: 10 (para 10%). Para valor fixo, digite ex: 15.00.',
            'max_uses': 'Deixe em branco para usos ilimitados.',
        }
