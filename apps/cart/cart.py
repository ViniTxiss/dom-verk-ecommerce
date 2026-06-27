from decimal import Decimal
from apps.products.models import Product, ProductVariant


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, variant_id, quantity=1, override_quantity=False):
        product_id = str(product.id)
        key = f"{product_id}_{variant_id}"
        if key not in self.cart:
            self.cart[key] = {
                'product_id': product_id,
                'variant_id': str(variant_id),
                'quantity': 0,
                'price': str(product.current_price),
            }
        if override_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity
        self.save()

    def remove(self, key):
        if key in self.cart:
            del self.cart[key]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = [v['product_id'] for v in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(p.id): p for p in products}

        variant_ids = [v['variant_id'] for v in self.cart.values()]
        try:
            variants = ProductVariant.objects.filter(id__in=variant_ids)
            variants_map = {str(v.id): v for v in variants}
        except Exception:
            variants_map = {}

        cart = self.cart.copy()
        for key, item in cart.items():
            item['product'] = products_map.get(item['product_id'])
            item['variant'] = variants_map.get(item['variant_id'])
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['key'] = key
            yield item

    def __len__(self):
        return self.get_total_items()
