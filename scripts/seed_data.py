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
        ('Polo', 'polo', 1),
        ('Manga Longa', 'manga-longa', 2),
        ('Hoodies', 'hoodies', 3),
        ('Calças', 'calcas', 4),
        ('Acessórios', 'acessorios', 5),
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
            'name': 'Camiseta Essential Black',
            'slug': 'camiseta-essential-black',
            'category': cat_map['camisetas'],
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
            'category': cat_map['camisetas'],
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
            'category': cat_map['camisetas'],
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
            'category': cat_map['polo'],
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
            'category': cat_map['manga-longa'],
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
            'category': cat_map['hoodies'],
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
            'category': cat_map['camisetas'],
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
            'category': cat_map['camisetas'],
            'price': 84.90,
            'story': 'O bege não é cor de parede — na DOM VERK, é declaração.',
            'description': 'Algodão natural sem tingimento artificial. Tom bege natural. Sustentável por natureza.',
            'image': 'products/camiseta_oversized.png',
            'is_featured': False,
            'colors': ['bege', 'areia'],
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
            sizes = ['PP', 'P', 'M', 'G', 'GG', '2GG', '3GG', '4GG']
            for color in colors:
                for size in sizes:
                    stock = 10 if size in ['M', 'G', 'GG'] else 5
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
