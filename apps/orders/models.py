from django.db import models
from django.conf import settings
from apps.products.models import ProductVariant


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Aguardando Pagamento'),
        ('paid', 'Pago'),
        ('processing', 'Em Processamento'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
    ]

    PAYMENT_CHOICES = [
        ('pix', 'PIX'),
        ('credit_card', 'Cartão de Crédito'),
        ('boleto', 'Boleto Bancário'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField('Forma de Pagamento', max_length=20, choices=PAYMENT_CHOICES, default='pix')

    # Dados do comprador
    buyer_name = models.CharField('Nome', max_length=200)
    buyer_email = models.CharField('E-mail', max_length=254)
    buyer_phone = models.CharField('Telefone', max_length=20, blank=True)
    buyer_cpf = models.CharField('CPF', max_length=14, blank=True)

    # Endereço de entrega
    address_street = models.CharField('Rua', max_length=255)
    address_number = models.CharField('Número', max_length=20)
    address_complement = models.CharField('Complemento', max_length=100, blank=True)
    address_neighborhood = models.CharField('Bairro', max_length=100)
    address_city = models.CharField('Cidade', max_length=100)
    address_state = models.CharField('Estado', max_length=2)
    address_zip = models.CharField('CEP', max_length=9)

    # Valores
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0)
    shipping = models.DecimalField('Frete', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Desconto', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0)

    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido #{self.id} — {self.buyer_name}"

    @property
    def order_number(self):
        return f"DV{self.id:06d}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField('Nome do Produto', max_length=200)
    product_color = models.CharField('Cor', max_length=50)
    product_size = models.CharField('Tamanho', max_length=10)
    price = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Quantidade', default=1)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f"{self.product_name} ({self.product_size}) x{self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity
