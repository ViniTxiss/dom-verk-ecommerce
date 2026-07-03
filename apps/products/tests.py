"""
Testes de produtos — modelos, propriedades e views principais.
Cobre: Product.current_price, has_discount, discount_percent, listagem e detalhe.
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from apps.products.models import Category, Product, ProductVariant


def make_category(**kwargs):
    defaults = {'name': 'Camisetas', 'slug': 'camisetas'}
    defaults.update(kwargs)
    return Category.objects.create(**defaults)


def make_product(category, **kwargs):
    defaults = {
        'name': 'Camiseta Teste',
        'slug': 'camiseta-teste',
        'price': Decimal('89.90'),
        'is_active': True,
    }
    defaults.update(kwargs)
    return Product.objects.create(category=category, **defaults)


def make_variant(product, color='preto', size='M', stock=10):
    return ProductVariant.objects.create(
        product=product, color=color, size=size,
        stock=stock, is_available=True
    )


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = make_category()
        self.product = make_product(self.category)

    def test_current_price_sem_promo(self):
        """Produto sem preço promocional retorna preço cheio."""
        self.assertEqual(self.product.current_price, Decimal('89.90'))

    def test_current_price_com_promo(self):
        """Produto com preço promocional retorna price_promo."""
        self.product.price_promo = Decimal('69.90')
        self.product.save()
        self.assertEqual(self.product.current_price, Decimal('69.90'))

    def test_has_discount_sem_promo(self):
        self.assertFalse(self.product.has_discount)

    def test_has_discount_com_promo(self):
        self.product.price_promo = Decimal('69.90')
        self.product.save()
        self.assertTrue(self.product.has_discount)

    def test_has_discount_promo_igual_preco(self):
        """price_promo igual ao price NÃO é desconto."""
        self.product.price_promo = Decimal('89.90')
        self.product.save()
        self.assertFalse(self.product.has_discount)

    def test_discount_percent(self):
        """Desconto de R$89,90 para R$71,92 deve ser ~20%."""
        self.product.price_promo = Decimal('71.92')
        self.product.save()
        self.assertEqual(self.product.discount_percent, 20)

    def test_discount_percent_sem_promo(self):
        self.assertEqual(self.product.discount_percent, 0)

    def test_str(self):
        self.assertEqual(str(self.product), 'Camiseta Teste')


class ProductListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = make_category()
        self.product = make_product(self.category, is_featured=True)
        make_variant(self.product)

    def test_listagem_retorna_200(self):
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)

    def test_listagem_exibe_produto_ativo(self):
        response = self.client.get(reverse('products:list'))
        self.assertContains(response, 'Camiseta Teste')

    def test_listagem_nao_exibe_produto_inativo(self):
        self.product.is_active = False
        self.product.save()
        response = self.client.get(reverse('products:list'))
        self.assertNotContains(response, 'Camiseta Teste')

    def test_filtro_por_categoria(self):
        """Filtro por categoria deve retornar apenas produtos desta categoria."""
        outra_cat = make_category(name='Polo', slug='polo')
        make_product(outra_cat, name='Polo Teste', slug='polo-teste')

        response = self.client.get(reverse('products:list') + '?categoria=camisetas')
        self.assertContains(response, 'Camiseta Teste')
        self.assertNotContains(response, 'Polo Teste')

    def test_filtro_por_tamanho(self):
        """Filtro por tamanho deve retornar produto com variante no tamanho."""
        response = self.client.get(reverse('products:list') + '?tamanho=M')
        self.assertContains(response, 'Camiseta Teste')

    def test_filtro_por_tamanho_sem_variante(self):
        """Produto sem variante no tamanho não deve aparecer."""
        response = self.client.get(reverse('products:list') + '?tamanho=PP')
        self.assertNotContains(response, 'Camiseta Teste')


class ProductDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = make_category()
        self.product = make_product(self.category)
        make_variant(self.product)

    def test_detalhe_retorna_200(self):
        response = self.client.get(
            reverse('products:detail', kwargs={'slug': self.product.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_detalhe_produto_inativo_retorna_404(self):
        self.product.is_active = False
        self.product.save()
        response = self.client.get(
            reverse('products:detail', kwargs={'slug': self.product.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_detalhe_slug_inexistente_retorna_404(self):
        response = self.client.get(
            reverse('products:detail', kwargs={'slug': 'slug-que-nao-existe'})
        )
        self.assertEqual(response.status_code, 404)
