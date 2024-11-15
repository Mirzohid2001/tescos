from django.contrib import admin
from .models import (
    News, ShelvingCategory, Shelving, ShelvingOrder, ShelvingGallery,
    CategoryProduct, Product, OrderProduct, ContactInquiry, Promotion, Project
)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ShelvingCategory)
class ShelvingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Shelving)
class ShelvingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'created_at', 'updated_at')
    search_fields = ('title', 'about')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ShelvingOrder)
class ShelvingOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'shelving', 'count', 'created_at')
    search_fields = ('name', 'phone', 'address')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ShelvingGallery)
class ShelvingGalleryAdmin(admin.ModelAdmin):
    list_display = ('shelving', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'short_description', 'full_description')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'short_description', 'full_description', 'image')
        }),
        ('Technical Specifications', {
            'fields': (
                'work_zone_length', 'floor_zone_length', 'width', 'height',
                'work_zone_width', 'working_surface', 'coating', 'color',
                'protective_bumper', 'contact'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'product', 'count', 'created_at')
    search_fields = ('name', 'phone', 'address')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'interested_product', 'submitted_at')
    search_fields = ('name', 'phone', 'email', 'interested_product')
    list_filter = ('submitted_at',)
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at',)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')
    filter_horizontal = ('products', 'shelvings')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    filter_horizontal = ('products', 'shelvings')
