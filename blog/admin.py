from django.contrib import admin

from .forms import ProductAdminForm
from .models import (
    News, Category, Product, Gallery, OrderProduct, Promotion, Project, ContactInquiry, About, ProductImage
)
from django.db import models
from ckeditor.widgets import CKEditorWidget


# Admin configuration for News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# Admin configuration for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)
    ordering = ('name',)


# Inline configuration for Gallery
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


# Admin configuration for Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='default')},
    }

    inlines = [ProductImageInline]

    list_display = ('name', 'category', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'category__name', 'short_description', 'full_description')
    list_filter = ('category', 'created_at', 'updated_at')
    ordering = ('-created_at',)


# admin.site.register(Product, ProductAdmin)


# Admin configuration for Gallery
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'created_at', 'updated_at')
    search_fields = ('product__name',)
    list_filter = ('created_at',)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'phone', 'address', 'count', 'created_at')
    search_fields = ('name', 'phone', 'address', 'product__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# Admin configuration for Promotion
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)
    filter_horizontal = ('products',)


# Admin configuration for Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    filter_horizontal = ('products',)


# Admin configuration for ContactInquiry
@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'submitted_at')
    search_fields = ('name', 'phone', 'email', 'message')
    list_filter = ('submitted_at', 'consent')
    ordering = ('-submitted_at',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'created_at', 'updated_at')
    search_fields = ('product__name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# Admin configuration for About
admin.site.register(About)
