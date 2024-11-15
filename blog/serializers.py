from rest_framework import serializers
from .models import News, ShelvingCategory, Shelving, ShelvingOrder, ShelvingGallery, CategoryProduct, Product, \
    OrderProduct, ContactInquiry, Promotion, Project


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'image', 'created_at', 'updated_at')


class ShelvingCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = ShelvingCategory
        fields = ('id', 'name', 'created_at', 'updated_at')


class ShelvingGallerySerializer(serializers.ModelSerializer):
    img = serializers.ImageField(use_url=True)

    class Meta:
        model = ShelvingGallery
        fields = ['img']


class ShelvingSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(use_url=True)
    gallery = ShelvingGallerySerializer(many=True, read_only=True)

    class Meta:
        model = Shelving
        fields = [
            'id',
            'title',
            'about',
            'Shelvesdepth',
            'Dimensions',
            'Loadcapacityofeachshelf',
            'bracket',
            'color',
            'img',
            'category',
            'order',
            'created_at',
            'updated_at',
            'gallery',
        ]


class ProductSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'short_description', 'image', 'created_at']

class ShelvingSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelving
        fields = ['id', 'title', 'about', 'img', 'created_at']

class ShelvingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelvingOrder
        fields = ['name', 'phone', 'address', 'shelving', 'count', 'created_at']


class CategoryProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = ['id', 'name', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'name', 'short_description', 'image', 'created_at', 'updated_at'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'name', 'short_description', 'image', 'full_description',
            'work_zone_length', 'floor_zone_length', 'width', 'height',
            'work_zone_width', 'working_surface', 'coating', 'color',
            'protective_bumper', 'created_at', 'updated_at'
        ]


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'name', 'phone', 'address', 'count']


class PromotionSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    shelvings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Promotion
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date',
            'discount_percentage', 'products', 'shelvings'
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
    shelvings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'image', 'products', 'shelvings', 'created_at', 'updated_at']
