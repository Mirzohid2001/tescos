from rest_framework import serializers
from .models import News, Category, Product
from .models import News, Gallery, Product, \
    OrderProduct, ContactInquiry, Promotion, Project


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'image', 'created_at', 'updated_at')


class CategoryProductSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories', 'created_at', 'updated_at']

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return CategoryProductSerializer(subcategories, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'short_description',
            'image',
            'contact',
            'category',
            'created_at',
            'updated_at'
        ]

    def get_category(self, obj):
        if obj.category:
            return {
                "id": obj.category.id,
                "name": obj.category.name,
                "parent": obj.category.parent.name if obj.category.parent else None
            }
        return None


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'image', 'created_at', 'updated_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True, read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'name',
            'short_description',
            'full_description',
            'image',
            'contact',
            'gallery',
            'created_at',
            'updated_at'
        ]

    def get_category(self, obj):
        if obj.category:
            return {
                "id": obj.category.id,
                "name": obj.category.name,
                "parent": {
                    "id": obj.category.parent.id,
                    "name": obj.category.parent.name
                } if obj.category.parent else None
            }
        return None


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'name', 'phone', 'address', 'count']


class PromotionSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Promotion
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date',
            'discount_percentage', 'products'
        ]


class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = [
            'name', 'phone', 'email', 'interested_product',
            'message', 'attached_file', 'consent', 'submitted_at'
        ]
        read_only_fields = ('submitted_at',)

    def validate_consent(self, value):
        if value is not True:
            raise serializers.ValidationError("You must agree to the processing of personal data.")
        return value


class ProjectSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'image', 'products', 'created_at', 'updated_at']
