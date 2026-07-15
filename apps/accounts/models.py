from django.contrib.auth.models import AbstractUser
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField


class CustomUser(AbstractUser):
    phone = models.CharField('Telefone', max_length=20, blank=True)
    # CPF criptografado em repouso — conformidade LGPD (M3)
    cpf = EncryptedCharField('CPF', max_length=14, blank=True)
    birth_date = models.DateField('Data de Nascimento', null=True, blank=True)

    # Endereço padrão
    address_street = models.CharField('Rua', max_length=255, blank=True)
    address_number = models.CharField('Número', max_length=20, blank=True)
    address_complement = models.CharField('Complemento', max_length=100, blank=True)
    address_neighborhood = models.CharField('Bairro', max_length=100, blank=True)
    address_city = models.CharField('Cidade', max_length=100, blank=True)
    address_state = models.CharField('Estado', max_length=2, blank=True)
    address_zip = models.CharField('CEP', max_length=9, blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def get_full_address(self):
        parts = [self.address_street, self.address_number]
        if self.address_complement:
            parts.append(self.address_complement)
        parts += [self.address_neighborhood, self.address_city, self.address_state]
        return ', '.join(filter(None, parts))
