from django.contrib import admin
from .models import News, Category, Product, Gallery, OrderProduct, Promotion, Project, ContactInquiry


# News Admin
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('name',)
    prepopulated_fields = {"name": ("parent",)}  # Optional for better handling of names


# Product Admin
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'contact', 'created_at', 'updated_at')
    search_fields = ('name', 'short_description', 'category__name')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)
    inlines = [GalleryInline]


# Gallery Admin
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'created_at')
    search_fields = ('product__name',)
    list_filter = ('created_at',)


# OrderProduct Admin
@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'phone', 'address', 'count', 'created_at')
    search_fields = ('name', 'product__name', 'phone', 'address')
    list_filter = ('created_at', 'product__category')
    ordering = ('-created_at',)


# Promotion Admin
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)
    filter_horizontal = ('products',)


# Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    filter_horizontal = ('products',)


# ContactInquiry Admin
@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'interested_product', 'submitted_at')
    search_fields = ('name', 'phone', 'email', 'interested_product', 'message')
    list_filter = ('submitted_at', 'consent')
    ordering = ('-submitted_at',)
