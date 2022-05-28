import django
from django.urls import path,include
from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, CustomerPasswordRestForm, CustomerSetPasswordForm

urlpatterns = [
                  # path('', views.home),
            path('', views.HomeView.as_view(), name='home'),
            path('mobile/', views.MobileView.as_view(), name='mobile'),
            path('product-detail/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
            path('mobile/', views.MobileView.as_view(), name='mobile'),
            path('top-wear/', views.TopWearView.as_view(), name='topwear'),
            path('bottom-wear/', views.BottomWearView.as_view(), name='bottomwear'),
            path('cart-view/', views.CartView.as_view(), name='cart-view'),
            path('cart/plus-quantity/', views.plus_quantity, name='plus_quantity'),
            path('cart/minus-quantity/', views.minus_quantity, name='minus_quantity'),
            path('cart-view/remove-item/', views.remove_item, name='remove_item'),
            path('profile/', views.Profile.as_view(), name='profile'),

            path('address/', views.Address.as_view(), name='address'),
            path('address/<int:id>/', views.UpdateAddress.as_view(), name='address_update'),
            path('address-deleted/<int:pk>/', views.DeleteAddress.as_view(), name='address_delete'),

            path('checkout/', views.OrderSummary.as_view(), name='checkout'),

            path('search/', views.search_product, name='search'),

            path('payment/',views.Payment.as_view(),name='payment'),
            path('buy', views.BuyNow.as_view(), name='buynow'),
            path('orders/', views.OrdersList.as_view(), name='orders'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
