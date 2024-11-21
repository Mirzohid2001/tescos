from django.urls import path
from .views import NewsAPIView, ProductAPIView, \
    ProductDetailView, CategoryProductAPIView, ContactInquiryCreateView, PromotionListView, PromotionDetailView, \
    ProjectListView, ProjectDetailView, ProductSearchView, CategorySearchView

urlpatterns = [
    path('news/', NewsAPIView.as_view(), name='news'),
    path('product/', ProductAPIView.as_view(), name='product'),
    path('category/', CategoryProductAPIView.as_view(), name='categoryproduct'),
    path('productdetail/<int:id>/', ProductDetailView.as_view(), name='productdetail'),
    path('contactinquiry/', ContactInquiryCreateView.as_view(), name='contactinquiry'),
    path('promotions/', PromotionListView.as_view(), name='promotion-list'),
    path('promotions/<int:id>/', PromotionDetailView.as_view(), name='promotion-detail'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:id>/', ProjectDetailView.as_view(), name='project-detail'),
    path('search/products/', ProductSearchView.as_view(), name='product-search'),
    path('search/categories/', CategorySearchView.as_view(), name='category-search'),
]
