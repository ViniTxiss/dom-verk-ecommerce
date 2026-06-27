from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from .models import Product, Category, Review


def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True).prefetch_related('variants')[:8]
    flash_deals = Product.objects.filter(is_active=True, is_flash_deal=True).prefetch_related('variants')[:4]
    categories = Category.objects.filter(is_active=True)[:6]
    new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:4]

    context = {
        'featured_products': featured_products,
        'flash_deals': flash_deals,
        'categories': categories,
        'new_arrivals': new_arrivals,
        'placeholder_categories': ['Camisetas', 'Polo', 'Manga Longa', 'Hoodies', 'Calças', 'Acessórios'],
    }
    return render(request, 'home/index.html', context)


def product_list(request):
    products = Product.objects.filter(is_active=True).prefetch_related('variants')
    categories = Category.objects.filter(is_active=True)
    category_slug = request.GET.get('categoria')
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Filtros
    size = request.GET.get('tamanho')
    color = request.GET.get('cor')
    sort = request.GET.get('ordenar', '-created_at')

    if size:
        products = products.filter(variants__size=size, variants__is_available=True).distinct()
    if color:
        products = products.filter(variants__color=color, variants__is_available=True).distinct()

    valid_sorts = ['-created_at', 'price', '-price', 'name']
    if sort not in valid_sorts:
        sort = '-created_at'
    products = products.order_by(sort)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'current_sort': sort,
        'current_size': size,
        'current_color': color,
    }
    return render(request, 'products/list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    gallery = product.gallery.all()
    reviews = product.reviews.filter(is_approved=True)
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    # Variantes disponíveis
    available_colors = product.variants.filter(is_available=True).values_list('color', flat=True).distinct()
    available_sizes = product.variants.filter(is_available=True).values_list('size', flat=True).distinct()

    context = {
        'product': product,
        'gallery': gallery,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': reviews.count(),
        'related_products': related_products,
        'available_colors': list(available_colors),
        'available_sizes': list(available_sizes),
    }
    return render(request, 'products/detail.html', context)


def privacy_policy(request):
    return render(request, 'institutional/privacy_policy.html')


def terms_of_use(request):
    return render(request, 'institutional/terms_of_use.html')


def exchanges(request):
    return render(request, 'institutional/exchanges.html')


def about(request):
    return render(request, 'institutional/about.html')


def size_guide(request):
    return render(request, 'institutional/size_guide.html')
