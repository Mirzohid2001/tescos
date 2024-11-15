from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News, ShelvingCategory, Shelving, ShelvingOrder, ShelvingGallery, CategoryProduct, Product, \
    ContactInquiry, Promotion, Project
from .serializers import NewsSerializers, ShelvingCategorySerializers, ShelvingSerializer, ShelvingOrderSerializer, \
    ShelvingGallery, ShelvingGallerySerializer, CategoryProductSerializers, ProductSerializer, ProductDetailSerializer, \
    OrderProductSerializer, ContactInquirySerializer, PromotionSerializer, ProjectSerializer, ProductSummarySerializer, \
    ShelvingSummarySerializer
from django.conf import settings
import requests
from django.db.models import Q


# Create your views here.

class NewsAPIView(APIView):
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializers(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShelvingCategoryAPIView(APIView):
    def get(self, request):
        shelvingcategory = ShelvingCategory.objects.all()
        serializer = ShelvingCategorySerializers(shelvingcategory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShelvingAPIView(APIView):
    def get(self, request):
        shelvings = Shelving.objects.all().order_by('-created_at')[:4]
        serializer = ShelvingSerializer(shelvings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PromotionListView(generics.ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class PromotionDetailView(generics.RetrieveAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    lookup_field = 'id'


class ShelvingDetailView(APIView):
    def get(self, request, id):
        try:
            shelving = Shelving.objects.get(id=id)
            serializer = ShelvingSerializer(shelving)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Shelving.DoesNotExist:
            return Response({'detail': 'Shelving not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        serializer = ShelvingOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                shelving = Shelving.objects.get(id=id)
            except Shelving.DoesNotExist:
                return Response({'detail': 'Shelving not found.'}, status=status.HTTP_404_NOT_FOUND)
            order = serializer.save(shelving=shelving)
            self.send_order_to_telegram(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_order_to_telegram(self, order):
        BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
        CHAT_ID = settings.TELEGRAM_CHAT_ID
        message = f"""
<b>Новый заказ стеллажа</b>
Имя: {order.name}
Телефон: {order.phone}
Адрес: {order.address}
Стеллаж: {order.shelving.title}
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
            print(f"Ошибка при отправке сообщения в Telegram: {e}")


class CategoryProductAPIVIew(APIView):
    def get(self, request):
        categoryproduct = CategoryProduct.objects.all()
        serializer = CategoryProductSerializers(categoryproduct, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductAPIView(APIView):
    def get(self, request):
        products = Product.objects.all().order_by('-created_at')[:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


# class LatestProductsAndShelvingsView(APIView):
#     def get(self, request, *args, **kwargs):
#         latest_products = Product.objects.all().order_by('-created_at')[:4]
#         latest_shelvings = Shelving.objects.all().order_by('-created_at')[:4]
#
#         products_serializer = ProductSummarySerializer(latest_products, many=True)
#         shelvings_serializer = ShelvingSummarySerializer(latest_shelvings, many=True)
#
#         return Response({
#             'latest_products': products_serializer.data,
#             'latest_shelvings': shelvings_serializer.data
#         })


class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)

        if query:
            # Mahsulotlarni qidirish
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(short_description__icontains=query) |
                Q(category__name__icontains=query)
            )

            # Stellajlarni qidirish
            shelvings = Shelving.objects.filter(
                Q(title__icontains=query) |
                Q(about__icontains=query) |
                Q(category__name__icontains=query)
            )

            products_serializer = ProductSummarySerializer(products, many=True)
            shelvings_serializer = ShelvingSummarySerializer(shelvings, many=True)

            return Response({
                'products': products_serializer.data,
                'shelvings': shelvings_serializer.data
            })

        return Response({
            'products': [],
            'shelvings': []
        })


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'
