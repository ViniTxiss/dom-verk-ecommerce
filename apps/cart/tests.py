"""
Testes do carrinho — lógica da classe Cart e views AJAX.
Cobre: add, remove, update, total, contagem de itens.
"""
import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from apps.products.models import Category, Product, ProductVariant


def make_product_with_variant(price='89.90', stock=10):
    cat, _ = Category.objects.get_or_create(slug='camisetas', defaults={'name': 'Camisetas'})
    product = Product.objects.create(
        name='Camiseta Teste',
        slug='camiseta-cart-teste',
        price=Decimal(price),
        is_active=True,
        category=cat,
    )
    variant = ProductVariant.objects.create(
        product=product, color='preto', size='M',
        stock=stock, is_available=True
    )
    return product, variant


class CartAddTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.product, self.variant = make_product_with_variant()

    def _add(self, product_id, variant_id, quantity=1):
        return self.client.post(
            reverse('cart:add'),
            data=json.dumps({
                'product_id': product_id,
                'variant_id': variant_id,
                'quantity': quantity,
            }),
            content_type='application/json',
        )

    def test_add_retorna_sucesso(self):
        response = self._add(self.product.id, self.variant.id)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

    def test_add_incrementa_contador(self):
        self._add(self.product.id, self.variant.id, quantity=2)
        data = self.client.post(
            reverse('cart:add'),
            data=json.dumps({
                'product_id': self.product.id,
                'variant_id': self.variant.id,
                'quantity': 1,
            }),
            content_type='application/json',
        ).json()
        self.assertEqual(data['cart_count'], 3)

    def test_add_produto_inexistente_retorna_404(self):
        response = self._add(product_id=99999, variant_id=99999)
        self.assertEqual(response.status_code, 404)

    def test_add_estoque_insuficiente(self):
        """Tentar adicionar mais do que o estoque disponível deve falhar."""
        response = self._add(self.product.id, self.variant.id, quantity=999)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])

    def test_add_dados_invalidos(self):
        response = self.client.post(
            reverse('cart:add'),
            data='nao_e_json',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


class CartRemoveTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.product, self.variant = make_product_with_variant()
        # Adiciona item ao carrinho
        self.client.post(
            reverse('cart:add'),
            data=json.dumps({
                'product_id': self.product.id,
                'variant_id': self.variant.id,
                'quantity': 1,
            }),
            content_type='application/json',
        )

    def test_remove_item_existente(self):
        key = f"{self.product.id}_{self.variant.id}"
        response = self.client.post(
            reverse('cart:remove'),
            data=json.dumps({'key': key}),
            content_type='application/json',
        )
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 0)

    def test_remove_item_inexistente_nao_quebra(self):
        """Remover chave que não existe não deve lançar erro."""
        response = self.client.post(
            reverse('cart:remove'),
            data=json.dumps({'key': 'chave-fantasma'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])


class CartUpdateTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.product, self.variant = make_product_with_variant()
        self.client.post(
            reverse('cart:add'),
            data=json.dumps({
                'product_id': self.product.id,
                'variant_id': self.variant.id,
                'quantity': 2,
            }),
            content_type='application/json',
        )
        self.key = f"{self.product.id}_{self.variant.id}"

    def test_update_quantidade(self):
        response = self.client.post(
            reverse('cart:update'),
            data=json.dumps({'key': self.key, 'quantity': 5}),
            content_type='application/json',
        )
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 5)

    def test_update_quantidade_zero_remove_item(self):
        """Atualizar para 0 deve remover o item do carrinho."""
        response = self.client.post(
            reverse('cart:update'),
            data=json.dumps({'key': self.key, 'quantity': 0}),
            content_type='application/json',
        )
        data = response.json()
        self.assertEqual(data['cart_count'], 0)

    def test_cart_total_correto(self):
        """Total deve refletir preço × quantidade."""
        self.client.post(
            reverse('cart:update'),
            data=json.dumps({'key': self.key, 'quantity': 3}),
            content_type='application/json',
        )
        response = self.client.post(
            reverse('cart:update'),
            data=json.dumps({'key': self.key, 'quantity': 3}),
            content_type='application/json',
        )
        data = response.json()
        expected = str(Decimal('89.90') * 3)
        self.assertEqual(data['cart_total'], expected)


class CartDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_pagina_carrinho_retorna_200(self):
        response = self.client.get(reverse('cart:detail'))
        self.assertEqual(response.status_code, 200)
