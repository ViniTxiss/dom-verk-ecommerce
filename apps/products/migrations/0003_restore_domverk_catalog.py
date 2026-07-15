from django.db import migrations


def restore_domverk_catalog(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Product = apps.get_model('products', 'Product')
    ProductVariant = apps.get_model('products', 'ProductVariant')
    Review = apps.get_model('products', 'Review')

    # Limpa o catálogo antigo em produção (FIOTECH)
    Product.objects.all().delete()
    Category.objects.all().delete()

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

    cat_map = {}
    for name, slug, order in CATEGORIES:
        cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'order': order})
        cat_map[slug] = cat

    for data in PRODUCTS:
        colors = data.pop('colors')
        category_slug = data.pop('category_slug')
        data['category'] = cat_map[category_slug]

        product, created = Product.objects.get_or_create(slug=data['slug'], defaults=data)
        if created:
            for color in colors:
                for size in SIZES:
                    stock = 10 if size in ['M', 'G', 'GG'] else 5
                    sku = f"DV-{product.id}-{color.upper()}-{size}"
                    ProductVariant.objects.get_or_create(
                        product=product, color=color, size=size,
                        defaults={'sku': sku, 'stock': stock, 'is_available': True}
                    )
            if product.is_featured:
                for name, rating, comment in REVIEWS:
                    Review.objects.get_or_create(
                        product=product, user_name=name,
                        defaults={'rating': rating, 'comment': comment}
                    )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_productvariant_color'),
    ]

    operations = [
        migrations.RunPython(restore_domverk_catalog, migrations.RunPython.noop),
    ]
