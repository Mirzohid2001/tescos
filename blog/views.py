from django.shortcuts import render
from rest_framework import status, generics, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import News, Category, Product, \
    ContactInquiry, Promotion, Project, About
from .serializers import NewsSerializers, ProductSerializer, ProductDetailSerializer, \
    OrderProductSerializer, ContactInquirySerializer, PromotionSerializer, ProjectSerializer, \
    CategoryProductSerializer, AboutSerializer
from django.conf import settings
import requests
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
import requests
from django.db.models import Q
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class NewsAPIView(APIView):
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializers(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PromotionListView(generics.ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class PromotionDetailView(generics.RetrieveAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    lookup_field = 'id'


class CategoryWithProductsPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10

class CategoryWithProductsAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'parent__name']
    filterset_fields = ['parent']
    pagination_class = CategoryWithProductsPagination

    def list(self, request, *args, **kwargs):
        categories = self.filter_queryset(self.get_queryset())

        data = []
        for category in categories:
            products = Product.objects.filter(category=category).order_by('-created_at')[:4]
            serialized_category = {
                "category": CategoryProductSerializer(category).data,
                "products": ProductSerializer(products, many=True).data
            }
            data.append(serialized_category)

        return Response(data, status=status.HTTP_200_OK)



class ProductsByCategoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class ProductsByCategoryAPIView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name', 'short_description', 'full_description']
    filterset_fields = ['price', 'is_available']
    ordering_fields = ['price', 'created_at']
    pagination_class = ProductsByCategoryPagination

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if not category_id:
            raise serializers.ValidationError({"detail": "Category ID is required."})

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError({"detail": "Category not found."})

        return Product.objects.filter(category=category).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        category_id = self.request.query_params.get('category_id')
        category = Category.objects.filter(id=category_id).first()
        if not category:
            return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        category_data = CategoryProductSerializer(category).data
        response = super().get(request, *args, **kwargs)
        response.data = {
            "category": category_data,
            "products": response.data
        }
        return response


class ProductDetailView(APIView):
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        serializer = OrderProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
            order = serializer.save(product=product)
            self.send_order_to_telegram(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_order_to_telegram(self, order):
        BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
        CHAT_ID = settings.TELEGRAM_CHAT_ID
        message = f"""
<b>Новый заказ продукта</b>
Имя: {order.name}
Телефон: {order.phone}
Адрес: {order.address}
Продукт: {order.product.name}
Количество: {order.count}
"""
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to Telegram: {e}")


class ContactInquiryCreateView(generics.CreateAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact_inquiry = serializer.save()
        return Response(
            {"message": "Thank you for your inquiry.", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'


# class ProductSearchView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['name', 'short_description', 'full_description', 'category__name']
#
#
# # Search for Categories
# class CategorySearchView(ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryProductSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['name', 'parent__name']


class AboutAPIVIew(APIView):
    def get(self, request):
        about = About.objects.first()
        serializer = AboutSerializer(about)
        return Response(serializer.data)
