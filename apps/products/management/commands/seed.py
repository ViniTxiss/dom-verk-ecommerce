"""
Management command: python manage.py seed
Popula o banco com categorias, produtos, variantes e avaliações.
Idempotente: seguro para rodar múltiplas vezes (deleta antes de recriar para substituição total).
"""
from django.core.management.base import BaseCommand
from apps.products.models import Category, Product, ProductVariant, Review


CATEGORIES = [
    ('Camisetas', 'camisetas', 0),
    ('Polo', 'polo', 1),
    ('Manga Longa', 'manga-longa', 2),
    ('Hoodies', 'hoodies', 3),
    ('Calças', 'calcas', 4),
    ('Acessórios', 'acessorios', 5),
]

PRODUCTS = [
    {
        'name': 'Camiseta Essential Black',
        'slug': 'camiseta-essential-black',
        'category_slug': 'camisetas',
        'price': 89.90,
        'story': 'O preto que você conhece, só que melhor. A Essential Black foi pensada para quem sabe que o básico é tudo — desde que feito do jeito certo.',
        'description': '100% algodão penteado 30.1. Gola careca reforçada. Costuras duplas nas mangas e barra.',
        'image': 'products/camiseta_oversized.png',
        'is_featured': True,
        'colors': ['preto', 'cinza'],
    },
    {
        'name': 'Camiseta Oversized Off-White',
        'slug': 'camiseta-oversized-off-white',
        'category_slug': 'camisetas',
        'price': 99.90,
        'price_promo': 79.90,
        'story': 'Há looks que não precisam gritar para serem notados. O Off-White é assim — silencioso, seguro de si, impossível de ignorar.',
        'description': 'Fit oversized com queda de ombro. Algodão pesado 240g/m². Ideal para layering ou solo.',
        'image': 'products/camiseta_oversized.png',
        'is_featured': True,
        'is_flash_deal': True,
        'colors': ['branco', 'areia'],
    },
    {
        'name': 'Camiseta Gráfica Urbana',
        'slug': 'camiseta-grafica-urbana',
        'category_slug': 'camisetas',
        'price': 119.90,
        'story': 'A cidade não para. A camiseta que vai com ela também não.',
        'description': 'Impressão em serigrafia de alta resolução. Algodão premium 200g/m². Caimento reto.',
        'image': 'products/camiseta_oversized.png',
        'is_featured': True,
        'colors': ['preto', 'branco'],
    },
    {
        'name': 'Polo Premium Piqué',
        'slug': 'polo-premium-pique',
        'category_slug': 'polo',
        'price': 159.90,
        'price_promo': 129.90,
        'story': 'Entre o casual e o elegante, existe a Polo Premium.',
        'description': 'Malha piqué 100% algodão. Botões em madrepérola. Bordado discreto no peito.',
        'image': 'products/babylook_dryfit.png',
        'is_featured': True,
        'is_flash_deal': True,
        'colors': ['branco', 'azul', 'preto'],
    },
    {
        'name': 'Manga Longa Essencial',
        'slug': 'manga-longa-essencial',
        'category_slug': 'manga-longa',
        'price': 109.90,
        'story': 'Para quando as mangas curtas não são suficientes.',
        'description': 'Algodão penteado 180g/m². Gola careca. Punho com abertura dupla.',
        'image': 'products/short_fitness.png',
        'is_featured': False,
        'colors': ['preto', 'cinza', 'vinho'],
    },
    {
        'name': 'Hoodie Heavyweight',
        'slug': 'hoodie-heavyweight',
        'category_slug': 'hoodies',
        'price': 249.90,
        'price_promo': 199.90,
        'story': 'O frio não é desculpa para abrir mão do estilo.',
        'description': 'Moletom 380g/m². Bolso canguru. Capuz com cordão. Forro interno macio.',
        'image': 'products/top_nadador_legging.png',
        'is_featured': True,
        'is_flash_deal': True,
        'colors': ['preto', 'cinza', 'azul'],
    },
    {
        'name': 'Camiseta Slim Fit Cinza',
        'slug': 'camiseta-slim-fit-cinza',
        'category_slug': 'camisetas',
        'price': 94.90,
        'story': 'O cinza que não é neutro — é escolha.',
        'description': 'Fit slim com elastano 5%. Algodão premium 200g/m².',
        'image': 'products/top_nadador.png',
        'is_featured': True,
        'colors': ['cinza', 'preto'],
    },
    {
        'name': 'Camiseta Bege Clássica',
        'slug': 'camiseta-bege-classica',
        'category_slug': 'camisetas',
        'price': 84.90,
        'story': 'O bege não é cor de parede — na DOM VERK, é declaração.',
        'description': 'Algodão natural sem tingimento artificial. Tom bege natural. Sustentável por natureza.',
        'image': 'products/camiseta_oversized.png',
        'is_featured': False,
        'colors': ['bege', 'areia'],
    },
]

REVIEWS = [
    ('Marcos S.', 5, 'Qualidade incrível! O tecido é muito macio e o caimento é perfeito. Recomendo muito.'),
    ('Ana R.', 5, 'Superou minhas expectativas. Entrega rápida e produto excelente. Nota 10!'),
    ('Carlos M.', 4, 'Muito boa qualidade, toque super agradável no corpo.'),
]

SIZES = ['PP', 'P', 'M', 'G', 'GG', '2GG', '3GG', '4GG']


class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais da DOM VERK (categorias, produtos, variantes e avaliações).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Exclui produtos e categorias existentes antes de repopular.',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n[DOM VERK] Iniciando seed...\n'))

        if options.get('reset'):
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('  [!] Dados antigos excluídos com sucesso.'))

        # Categorias
        cat_map = {}
        for name, slug, order in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=slug, defaults={'name': name, 'order': order}
            )
            cat_map[slug] = cat
            status = 'criada' if created else 'já existe'
            self.stdout.write(f'  Categoria "{name}" — {status}')

        # Produtos
        self.stdout.write('')
        for data in PRODUCTS:
            colors = data.pop('colors')
            category_slug = data.pop('category_slug')
            data['category'] = cat_map[category_slug]

            product, created = Product.objects.get_or_create(
                slug=data['slug'], defaults=data
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'  [+] Produto: {product.name}'))
                for color in colors:
                    for size in SIZES:
                        stock = 15 if size in ['M', 'G'] else 8
                        ProductVariant.objects.get_or_create(
                            product=product, color=color, size=size,
                            defaults={'stock': stock, 'is_available': True}
                        )
                if product.is_featured:
                    for name, rating, comment in REVIEWS:
                        Review.objects.get_or_create(
                            product=product, user_name=name,
                            defaults={'rating': rating, 'comment': comment}
                        )
            else:
                self.stdout.write(f'  [=] Produto já existe: {product.name}')

        # Cupons de Desconto
        from apps.orders.models import Coupon
        from decimal import Decimal
        COUPONS = [
            {'code': 'DOM10', 'discount_type': 'percentage', 'discount_value': Decimal('10.00'), 'min_purchase_value': Decimal('0.00')},
            {'code': 'VERK20', 'discount_type': 'fixed', 'discount_value': Decimal('20.00'), 'min_purchase_value': Decimal('100.00')},
            {'code': 'BENVINDO15', 'discount_type': 'percentage', 'discount_value': Decimal('15.00'), 'min_purchase_value': Decimal('50.00')},
        ]
        self.stdout.write('')
        for c_data in COUPONS:
            coupon, created = Coupon.objects.get_or_create(
                code=c_data['code'],
                defaults=c_data
            )
            c_status = 'criado' if created else 'ja existe'
            self.stdout.write(self.style.SUCCESS(f'  [CUPOM] Cupom "{coupon.code}" -- {c_status}'))

        self.stdout.write(self.style.SUCCESS('\n[DOM VERK] Seed concluido! Acesse /loja/ para conferir.\n'))
