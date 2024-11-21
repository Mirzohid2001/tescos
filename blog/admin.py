from django.contrib import admin
from .models import (
    News, Category, Product, Gallery, OrderProduct, Promotion, Project, ContactInquiry
)


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
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1


# Admin configuration for Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'short_description', 'price')
    search_fields = ('name', 'short_description', 'category__name')
    list_filter = ('category',)
    ordering = ('name',)
    inlines = [GalleryInline]


# Admin configuration for Gallery
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'created_at', 'updated_at')
    search_fields = ('product__name',)
    list_filter = ('created_at',)


# Admin configuration for OrderProduct
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
    list_display = ('name', 'phone', 'email', 'interested_product', 'submitted_at')
    search_fields = ('name', 'phone', 'email', 'interested_product', 'message')
    list_filter = ('submitted_at', 'consent')
    ordering = ('-submitted_at',)
