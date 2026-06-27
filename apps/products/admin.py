from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 4


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'price_promo', 'is_active', 'is_featured', 'is_flash_deal']
    list_filter = ['category', 'is_active', 'is_featured', 'is_flash_deal']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline, ProductImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'product', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating']
