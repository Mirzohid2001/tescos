from django.urls import path
from .views import NewsAPIView, ShelvingCategoryAPIView, ShelvingDetailView, ShelvingAPIView, ProductAPIView, \
    ProductDetailView, CategoryProductAPIVIew, ContactInquiryCreateView, PromotionListView, PromotionDetailView, \
    ProjectListView, ProjectDetailView, SearchView

urlpatterns = [
    path('news/', NewsAPIView.as_view(), name='news'),
    path('shelvingcategory/', ShelvingCategoryAPIView.as_view(), name='shelvingcategory'),
    path('shelving/', ShelvingAPIView.as_view(), name='shelving'),
    path('shelving/<int:id>/', ShelvingDetailView.as_view(), name='shelving-detail'),
    path('product/', ProductAPIView.as_view(), name='product'),
    path('categoryproduct/', CategoryProductAPIVIew.as_view(), name='categoryproduct'),
    path('productdetail/<int:id>/', ProductDetailView.as_view(), name='productdetail'),
    path('contactinquiry/', ContactInquiryCreateView.as_view(), name='contactinquiry'),
    path('promotions/', PromotionListView.as_view(), name='promotion-list'),
    path('promotions/<int:id>/', PromotionDetailView.as_view(), name='promotion-detail'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:id>/', ProjectDetailView.as_view(), name='project-detail'),
    # path('latest-items/', LatestProductsAndShelvingsView.as_view(), name='latest-items'),
    path('search/', SearchView.as_view(), name='search'),

]
