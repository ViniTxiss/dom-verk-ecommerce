"""
DOM VERK — Script de dados iniciais
Cria categorias, produtos com variantes e reviews mockados
"""
import os
import django
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.products.models import Category, Product, ProductVariant, Review

def clean_database():
    print('  Limpando produtos, variantes e categorias antigas...')
    Product.objects.all().delete()
    Category.objects.all().delete()

def create_categories():
    cats = [
        ('Camisetas', 'camisetas', 0),
        ('Fitness', 'fitness', 1),
        ('Feminino', 'feminino', 2),
        ('Conjuntos', 'conjuntos', 3),
    ]
    created = []
    for name, slug, order in cats:
        cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'order': order})
        created.append(cat)
        print(f'  [OK] Categoria: {name}')
    return created

def create_products(categories):
    cat_map = {c.slug: c for c in categories}

    products_data = [
        {
            'name': 'Camiseta Feminina Academia Poliester Babylook Dryfit Fiotech',
            'slug': 'camiseta-feminina-academia-poliester-babylook-dryfit-fiotech',
            'category': cat_map['feminino'],
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
            'category': cat_map['conjuntos'],
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
            'category': cat_map['fitness'],
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
            'category': cat_map['fitness'],
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
            'category': cat_map['camisetas'],
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

    for data in products_data:
        colors = data.pop('colors')
        promo = data.pop('price_promo', None)
        if promo:
            data['price_promo'] = promo

        product, created = Product.objects.get_or_create(
            slug=data['slug'],
            defaults=data
        )

        if created:
            print(f'  [OK] Produto: {product.name}')
            
            # Criar variantes
            sizes = ['P', 'M', 'G', 'GG']
            for color in colors:
                for size in sizes:
                    stock = 15 if size in ['M', 'G'] else 8
                    ProductVariant.objects.get_or_create(
                        product=product,
                        color=color,
                        size=size,
                        defaults={'stock': stock, 'is_available': True}
                    )

            # Reviews
            if product.is_featured:
                reviews = [
                    ('Marcos S.', 5, 'Qualidade incrível! O tecido é muito macio e o caimento é perfeito. Recomendo muito.'),
                    ('Ana R.', 5, 'Superou minhas expectativas. Entrega rápida e produto excelente. Nota 10!'),
                    ('Carlos M.', 4, 'Muito boa qualidade, toque super agradável no corpo.'),
                ]
                for name, rating, comment in reviews:
                    Review.objects.get_or_create(
                        product=product,
                        user_name=name,
                        defaults={'rating': rating, 'comment': comment}
                    )
        else:
            print(f'  [INFO] Produto ja existe: {product.name}')

if __name__ == '__main__':
    print('\n[DOM VERK] Criando dados iniciais...\n')
    clean_database()
    print('\nCategorias:')
    categories = create_categories()
    print('\nProdutos:')
    create_products(categories)
    print('\n[DOM VERK] Dados iniciais criados com sucesso!')
    print('Acesse http://127.0.0.1:8000/ para ver a loja\n')
