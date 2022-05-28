import smtplib,os,sys

from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
from django.utils.decorators import decorator_from_middleware, method_decorator
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView,CreateView
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView,PasswordResetView
from django.shortcuts import get_object_or_404


from core.models import Product, OrderPlaced, Cart, Customer, User
from core.forms import CustomerRegistrationForm, LoginForm,ProfileForm,CustomerPasswordChangeForm,CustomerPasswordRestForm
from core.auth import auth_middleware,Cart_count

from account.utils import LoginRequiredMixin
import Ecommerce.settings as file


class HomeView(View):
    """
        - this is a Home page view class
        - show list of all top-wear and bottom-wear product list using list view
    """
    def get(self, request, *args, **kwargs):
        TopWear = Product.objects.filter(category="TW")
        BottomWear = Product.objects.filter(category="BW")
        context = {
            'TopWear': TopWear,
            'BottomWear': BottomWear,
            'user': request.user
        }
        return render(request, 'core/home.html', context)


class MobileView(ListView):
    """
        - Mobile list view
    """
    context_object_name = "Mobile"
    model = Product
    template_name = "core/mobile.html"

    def get_queryset(self):
        queryset = Product.objects.filter(category="M")
        return queryset

class TopWearView(ListView):
    """
        - top wear list view
    """
    context_object_name = "TopWear"
    model = Product
    template_name = "core/top_wear.html"

    def get_queryset(self):
        queryset = Product.objects.filter(category="TW")
        return queryset 

class BottomWearView(ListView):
    """
        - bottom wear list view
    """
    template_name = "core/bottom_wear.html"
    context_object_name = "BottomWear"
    model = Product

    def get_queryset(self):
        queryset = Product.objects.filter(category="BW")
        return queryset


class ProductDetail(DetailView):
    model = Product
    template_name = 'core/productdetail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetail,self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            element = Cart.objects.filter(user= user, product= context['product']).exists()
            context['element'] = element
        context['next'] = self.request.path
        return context


class CartView(LoginRequiredMixin):
    """
        - User cart view
        - list of all cart with quantity
    """
    def get(self, request):
        products = Cart.objects.select_related('user').filter(
                user=request.user
            ).order_by('-id')
        if products.count() == 0 :
            return render(request,'core/empty_cart.html')
        else:
            context = {}
            shipping_charge = 40
            context['products'] = products
            context['shipping_charge'] = shipping_charge
            return render(request, 'core/addtocart.html', context)

    def post(self, request):
        product = get_object_or_404(Product, id= int(request.POST.get('product_id')))
        Cart.objects.get_or_create(user = request.user,product = product)
        total_products = Cart.objects.filter(user=request.user).order_by('-id').count()
        request.session['cart_count'] = total_products
        messages.success(request, "product added to your cart successfully")
        return redirect('cart-view')


def cart_amount(request):
    """
     - this function will be used for count total amount of cart
    """
    user = request.user
    cart_products = Cart.objects.filter(user=user)
    cart_amount = 0
    Shipping_charge = 40
    for i in cart_products:
        cart_amount = cart_amount + (i.product.discounted_price * i.quantity)

    context = {
        'total_amount': cart_amount,
        'Shipping_charge': Shipping_charge,
    }
    return context


def plus_quantity(request):
    """ 
        - this function will be used for incerement quantity for specific product
    """
    if request.method == 'GET' and request.is_ajax():
        product = get_object_or_404(
            Product,
            id=int(request.GET.get(('student_id')))
        )
        cart = get_object_or_404(
            Cart,
            product=product,
            user=request.user
        )
        quantity = cart.quantity + 1
        cart.quantity = quantity
        cart.save()
        context = {
            'quantity': quantity,
            'cart_amount': cart_amount(request)
        }
        return JsonResponse(context)


def minus_quantity(request):
    """
        - this function will be used for decrement quantity for specific product
    """
    if request.method == 'GET' and request.is_ajax():
        user = request.user.username
        product = get_object_or_404(
            Product,
            id=int(request.GET.get('student_id'))
        )
        cart = get_object_or_404(
            Cart,
            product=product,
            user=request.user,
        )
        quantity = cart.quantity
        if quantity > 1:
            quantity = quantity - 1
            cart.quantity = quantity
            cart.save()
        else:
            quantity = quantity
        context = {
            'quantity': quantity,
            'cart_amount': cart_amount(request)

        }
        return JsonResponse(context)


def remove_item(request):
    """
        - this function will be used for Deleteing product from cart
    """
    if request.method == "GET" and request.is_ajax():
        Cart.objects.get(
            id=request.GET.get('item_id'),
            user=request.user
        ).delete()
        is_cart_empty = True if not Cart.objects.filter(user=request.user) else False
        context = {
             'cart_amount': cart_amount(request),
             'is_cart_empty': is_cart_empty,
        }
        return JsonResponse(context)


class Profile(LoginRequiredMixin):
    """
        - profile view
        : here you can add your multiple address
    """
    form_class = ProfileForm
    template_name = "core/profile.html"

    def get(self,request,*args,**kwargs):
        return render(request, self.template_name, {'form': self.form_class})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, username = request.user)
            obj = form.save(commit = False)
            obj.user = user
            obj.save()
            messages.success(request, "Address added successfully.")
            try:
                next = request.GET['next']
                return redirect(next)
            except:
                return redirect('address')


class Address(LoginRequiredMixin):
    """
        - here you will get list of all address
        : you can add new adderss delete address or update address
    """
    def get(self,request):
        address = Customer.objects.filter(user=request.user)
        return render(request,'core/address.html',{'addresses' : address})


class UpdateAddress(UpdateView):
    """
        - updateing customer address
    """
    model = Customer
    form_class = ProfileForm
    template_name = 'core/profile.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def form_valid(self, form):
        form.save()
        messages.success(self.request,"Address updated")
        return redirect('address')


class DeleteAddress(DeleteView):
    """
        - delete address view\
    """
    model = Customer
    template_name = 'core/address_delete_confirmation.html'
    success_url = reverse_lazy('address')


class OrderSummary(LoginRequiredMixin):
    """
        - List of all orders
    """
    def get(self,request):
        products = Cart.objects.filter(user= request.user)
        address = Customer.objects.filter(user = request.user)
        try:
            product_id = request.GET.get('buy_now')
            product = get_object_or_404(Product, id = product_id)
            context = {
                    'product' : product,
                    'addresses': address,
            }
            return render(request,'core/buynow.html',context)
        except:
            context = {
                'products' : products,
                'addresses': address
            }
            return render(request,'core/checkout.html',context)


class Payment(LoginRequiredMixin):
    
    def get(self,request, *args, **kwargs):
            customer_id = request.GET.get('address')
            if customer_id is None:
                messages.error(request, "Please select address")
                return redirect("checkout")

            customer = get_object_or_404(Customer,id=int(customer_id))

            products = Cart.objects.filter(user = request.user)
            for product in products:
                obj = OrderPlaced(
                    user= request.user,
                    customer= customer,
                    product= product.product,
                    quantity= product.quantity
                )
                obj.save()
                Cart.delete(product)
            content = '''
                        Your order is placed successfully.
                        your order is Accepted by our system.
                        we will contact you soon..
                '''
            mail = smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            email = file.email
            password = file.password
            try:
                print("first-first-first-first-first-first-first-first-first-first-first-")
                mail.login(email,password)
                print("secound-secound-secound-secound-secound-secound-secound-secound-")
                mail.sendmail(email,request.user.email,content)
                print("third-third-third-third-third-third-third-third-third-third-")
                mail.close()
                print("four-four-four-four-four-four-four-four-four-four-four-")
                messages.success(request,"Confirmation mail is sended to your Email please check")
            except:
                print("fiver-fiver-fiver-fiver-fiver-fiver-fiver-fiver-fiver-")
                messages.success(request,"due to some technicle issue Confirmation mail is not sended to your Email! but you order is booked")
            return redirect('orders')


class OrdersList(LoginRequiredMixin):
    """
        - OrdersList of specific user
    """
    def get(self,request):
        orders = OrderPlaced.objects.filter(user = request.user).order_by('-id')
        return render(request, 'core/orders.html',{'orders':orders})


class BuyNow(LoginRequiredMixin):

    def get(self,request , *args, **kwargs):
        product_id = request.GET.get('buy_now_product')
        customer_id = request.GET.get('address')
        if customer_id is None:
            messages.error(request, "Please select address")
            return HttpResponseRedirect(f'checkout/?buy_now={product_id}')

        product = get_object_or_404(Product, id = product_id)
        customer = get_object_or_404(Customer, id = customer_id)
        OrderPlaced(user = request.user, customer=customer,product=product).save()
        content = '''
            Your order is placed successfully.
            your order is Accepted by our system.
            we will contact you soon..
        '''
        mail = smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        email = file.email
        password = file.password
        try:
                mail.login(email,password)
                mail.sendmail(email,request.user.email,content)
                mail.close()
                messages.success(request,"Confirmation mail is sended to your Email please check")
        except:
                messages.success(request,"due to some technicle issue Confirmation mail is not sended to your Email! but you order is booked")
        return redirect('orders')

def search_product(request):
    text = request.GET['search']
    items = Product.objects.filter(title__icontains = text)
    return render(request,'core/search.html',{'items' : items})


