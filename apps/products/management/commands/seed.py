"""
Management command: python manage.py seed
Popula o banco com categorias, produtos, variantes e avaliações.
Idempotente: seguro para rodar múltiplas vezes (deleta antes de recriar para substituição total).
"""
from django.core.management.base import BaseCommand
from apps.products.models import Category, Product, ProductVariant, Review


CATEGORIES = [
    ('Camisetas', 'camisetas', 0),
    ('Fitness', 'fitness', 1),
    ('Feminino', 'feminino', 2),
    ('Conjuntos', 'conjuntos', 3),
]

PRODUCTS = [
    {
        'name': 'Camiseta Feminina Academia Poliester Babylook Dryfit Fiotech',
        'slug': 'camiseta-feminina-academia-poliester-babylook-dryfit-fiotech',
        'category_slug': 'feminino',
        'price': 47.60,
        'story': 'Desenvolvida para treinos intensos ou uso casual diário. O tecido Dry-Fit garante frescor e caimento ideal para destacar sua performance.',
        'description': 'Camiseta baby look fitness básica feminina, ideal para treinos. Possui mangas curtas e gola redonda, com ajuste confortável que se adapta ao corpo. Composição: 90% Poliéster, 10% Elastano.',
        'image': 'products/babylook_dryfit.png',
        'is_featured': True,
        'colors': ['preto', 'branco', 'rosa', 'azul'],
    },
    {
        'name': 'Conjunto Fiotech Top E Legging Feminino Poliamida',
        'slug': 'conjunto-fiotech-top-e-legging-feminino-poliamida',
        'category_slug': 'conjuntos',
        'price': 150.00,
        'price_promo': 142.50,
        'story': 'O conjunto que une alta sustentação do top nadador com a compressão perfeita da calça legging. Feito em poliamida de alta qualidade para máximo rendimento.',
        'description': 'Conjunto composto por top nadador e calça legging, desenvolvido para oferecer conforto e estilo durante atividades físicas. Material de alta durabilidade e toque agradável. Composição: 83% Poliamida, 17% Elastano.',
        'image': 'products/top_nadador_legging.png',
        'is_featured': True,
        'colors': ['preto'],
    },
    {
        'name': 'Short Fitness Fiotech Poliamida Academia Zero Transparência',
        'slug': 'short-fitness-fiotech-poliamida-academia-zero-transparencia',
        'category_slug': 'fitness',
        'price': 75.74,
        'story': 'Treine sem preocupações. O short fitness FIOTECH garante zero transparência e toque super suave, perfeito para agachamentos e corridas.',
        'description': 'Shorts fabricados para garantir zero transparência, oferecendo excelente elasticidade e respirabilidade para liberdade de movimento. Composição: 83% Poliamida, 17% Elastano.',
        'image': 'products/short_fitness.png',
        'is_featured': True,
        'is_flash_deal': True,
        'colors': ['cafe', 'capuccino', 'preto'],
    },
    {
        'name': 'Top Nadador Fiotech Feminino Poliamida Blackout',
        'slug': 'top-nadador-fiotech-feminino-poliamida-blackout',
        'category_slug': 'fitness',
        'price': 24.93,
        'story': 'Alta sustentação com a segurança da poliamida blackout. Costuras reforçadas que não incomodam durante as atividades.',
        'description': 'Top com design nadador que oferece alta sustentação e conforto para práticas esportivas. Composição: 83% Poliamida, 17% Elastano.',
        'image': 'products/top_nadador.png',
        'is_featured': False,
        'colors': ['preto'],
    },
    {
        'name': 'Camiseta Oversized Masculina Fiotech 100% Algodão',
        'slug': 'camiseta-oversized-masculina-fiotech-100-algodao',
        'category_slug': 'camisetas',
        'price': 64.53,
        'price_promo': 43.02,
        'story': 'Corte oversized autêntico para quem vive a cultura urbana. Confeccionada em algodão premium de alta gramatura para um caimento pesado e estilo streetwear impecável.',
        'description': 'Camiseta estilo streetwear unissex/masculina com corte oversized, focada em conforto e estilo casual. Composição: 100% Algodão Premium.',
        'image': 'products/camiseta_oversized.png',
        'is_featured': True,
        'is_flash_deal': True,
        'colors': ['preto', 'branco', 'cinza', 'areia'],
    },
]

REVIEWS = [
    ('Marcos S.', 5, 'Qualidade incrível! O tecido é muito macio e o caimento é perfeito. Recomendo muito.'),
    ('Ana R.', 5, 'Superou minhas expectativas. Entrega rápida e produto excelente. Nota 10!'),
    ('Carlos M.', 4, 'Muito boa qualidade, toque super agradável no corpo.'),
]

SIZES = ['P', 'M', 'G', 'GG']


class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais da DOM VERK (categorias, produtos, variantes e avaliações).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n[DOM VERK] Iniciando seed de substituição...\n'))

        # Limpar registros existentes para substituição completa
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

        self.stdout.write(self.style.SUCCESS('\n[DOM VERK] Seed concluído! Acesse /loja/ para conferir.\n'))
