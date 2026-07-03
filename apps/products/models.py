from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField('Imagem', upload_to='categories/', blank=True, null=True)
    description = models.TextField('Descrição', blank=True)
    order = models.PositiveIntegerField('Ordem', default=0)
    is_active = models.BooleanField('Ativa', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name='Categoria')
    name = models.CharField('Nome', max_length=200)
    slug = models.SlugField(unique=True, max_length=250)
    description = models.TextField('Descrição', blank=True)
    story = models.TextField('História do Produto', blank=True, help_text='Copy cultural — conta a história da peça (estilo Chico Rei)')
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    price_promo = models.DecimalField('Preço Promocional', max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField('Imagem Principal', upload_to='products/')
    image_hover = models.ImageField('Imagem Hover', upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField('Ativo', default=True)
    is_featured = models.BooleanField('Destaque', default=False)
    is_flash_deal = models.BooleanField('Flash Deal', default=False)
    flash_deal_ends = models.DateTimeField('Flash Deal termina em', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def current_price(self):
        return self.price_promo if self.price_promo else self.price

    @property
    def has_discount(self):
        return self.price_promo is not None and self.price_promo < self.price

    @property
    def discount_percent(self):
        if self.has_discount:
            return int((1 - self.price_promo / self.price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery', verbose_name='Produto')
    image = models.ImageField('Imagem', upload_to='products/gallery/')
    alt_text = models.CharField('Texto alternativo', max_length=200, blank=True)
    order = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens do Produto'
        ordering = ['order']


COLOR_CHOICES = [
    ('preto', 'Preto'),
    ('branco', 'Branco'),
    ('cinza', 'Cinza'),
    ('azul', 'Azul Marinho'),
    ('verde', 'Verde'),
    ('vinho', 'Vinho'),
    ('bege', 'Bege'),
    ('areia', 'Areia'),
    ('rosa', 'Rosa'),
    ('cafe', 'Café'),
    ('capuccino', 'Capuccino'),
]

SIZE_CHOICES = [
    ('PP', 'PP'),
    ('P', 'P'),
    ('M', 'M'),
    ('G', 'G'),
    ('GG', 'GG'),
    ('2GG', '2GG'),
    ('3GG', '3GG'),
    ('4GG', '4GG'),
]


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='Produto')
    color = models.CharField('Cor', max_length=20, choices=COLOR_CHOICES)
    size = models.CharField('Tamanho', max_length=5, choices=SIZE_CHOICES)
    sku = models.CharField('SKU', max_length=50, unique=True, blank=True)
    stock = models.PositiveIntegerField('Estoque', default=0)
    is_available = models.BooleanField('Disponível', default=True)

    class Meta:
        verbose_name = 'Variante'
        verbose_name_plural = 'Variantes'
        unique_together = ['product', 'color', 'size']

    def __str__(self):
        return f"{self.product.name} — {self.color} / {self.size}"

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"DV-{self.product.id}-{self.color.upper()}-{self.size}"
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Produto')
    user_name = models.CharField('Nome', max_length=100)
    rating = models.PositiveSmallIntegerField('Avaliação', choices=[(i, i) for i in range(1, 6)], default=5)
    comment = models.TextField('Comentário')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField('Aprovado', default=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name} — {self.product.name} ({self.rating}★)"
