from django.urls import path
from .views import NewsAPIView, \
    ProductDetailView, ContactInquiryCreateView, PromotionListView, PromotionDetailView, \
    ProjectListView, ProjectDetailView, CategoryWithProductsAPIView, \
    ProductsByCategoryAPIView,AboutAPIVIew

urlpatterns = [
    path('news/', NewsAPIView.as_view(), name='news'),
    path('products-by-category/', ProductsByCategoryAPIView.as_view(), name='products_by_category'),
    path('about/', AboutAPIVIew.as_view(), name='about'),
    path('categories-with-products/', CategoryWithProductsAPIView.as_view(), name='categories_with_products'),
    path('productdetail/<int:id>/', ProductDetailView.as_view(), name='productdetail'),
    path('contactinquiry/', ContactInquiryCreateView.as_view(), name='contactinquiry'),
    path('promotions/', PromotionListView.as_view(), name='promotion-list'),
    path('promotions/<int:id>/', PromotionDetailView.as_view(), name='promotion-detail'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:id>/', ProjectDetailView.as_view(), name='project-detail'),
]
