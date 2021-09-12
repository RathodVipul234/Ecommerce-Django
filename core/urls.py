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

                  path('registration/', views.CustomerRegistration.as_view(), name='customerregistration'),
                  # path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form = LoginForm), name='login'),
                  # path('accounts/login/',views.CustomerLogin.as_view(), name='login'),
                  path('accounts/login/', views.CustomerLogin, name='login'),
                  path('accounts/logout/', views.Logout, name='logout'),

                  path('cart-view/', views.CartView.as_view(), name='cart-view'),
                  # path('add-to-cart/', views.AddToCart.as_view(), name='add-to-cart'),
                  path('cart/plus-quantity/', views.plus_quantity, name='plus_quantity'),
                  path('cart/minus-quantity/', views.minus_quantity, name='minus_quantity'),
                  path('cart-view/remove-item/', views.remove_item, name='remove_item'),
                  path('profile/', views.Profile.as_view(), name='profile'),

                  path('address/', views.Address.as_view(), name='address'),
                  path('address/<int:id>/', views.UpdateAddress.as_view(), name='address_update'),
                  path('address-deleted/<int:pk>/', views.DeleteAddress.as_view(), name='address_delete'),


                  # reset password
                  # path('',include('django.contrib.auth.urls')),

                  path('password-reset/', auth_views.PasswordResetView.as_view(
                      template_name='core/password_reset.html',
                      form_class=CustomerPasswordRestForm
                  ), name='password_reset'),

                  path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
                      template_name='core/password_reset_done.html',
                  ), name='password_reset_done'),

                  path('accounts/password-reset/confirm/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(
                           template_name='core/password_reset_confirm.html',
                           form_class=CustomerSetPasswordForm), name='password_reset_confirm'),

                  path('password-reset-complete/', auth_views.
                       PasswordResetCompleteView.as_view(
                       template_name='core/password_reset_complete.html',
                  ), name='password_reset_complete'),


                  # path('changePassword/', auth_views.PasswordChangeView.as_view(
                  #     template_name = 'core/changepassword1.html',
                  #     success_url = '/'
                  # ), name='changepassword'),#this is also working

                  path('checkout/', views.OrderSummary.as_view(), name='checkout'),

                  path('search/', views.search_product, name='search'),

                  path('payment/',views.Payment.as_view(),name='payment'),
                  path('buy', views.BuyNow.as_view(), name='buynow'),
                  path('orders/', views.OrdersList.as_view(), name='orders'),
                  path('changePassword/', views.ChangePassword.as_view(), name='changepassword'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
