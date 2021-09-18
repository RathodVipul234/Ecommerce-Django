from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, DetailView,CreateView
from django.views.generic.edit import UpdateView,DeleteView
from .models import Product, OrderPlaced, Cart, Customer, User
from .forms import CustomerRegistrationForm, LoginForm,ProfileForm,CustomerPasswordChangeForm,CustomerPasswordRestForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.decorators import login_required
from django.utils.decorators import decorator_from_middleware, method_decorator
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView,PasswordResetView
from django.urls import reverse_lazy
from .auth import auth_middleware,Cart_count
import smtplib,os,sys
import Ecommerce.settings as file


class HomeView(ListView):
    def get(self, request, *args, **kwargs):
        TopWear = Product.objects.filter(category="TW")
        BottomWear = Product.objects.filter(category="BW")
        user = request.user

        context = {
            'TopWear': TopWear,
            'BottomWear': BottomWear,
            'user': user
        }
        return render(request, 'core/home.html', context)


class MobileView(ListView):
    @method_decorator(Cart_count)
    def get(self, request, *args, **kwargs):
        Mobile = Product.objects.filter(category="M")
        context = {
            'Mobile': Mobile,
        }
        return render(request, 'core/mobile.html', context)

class TopWearView(ListView):
    @method_decorator(Cart_count)
    def get(self, request, *args, **kwargs):
        TopWear = Product.objects.filter(category="TW")
        context = {
            'TopWear': TopWear,
        }
        return render(request, 'core/top_wear.html', context)

class BottomWearView(ListView):
    @method_decorator(Cart_count)
    def get(self, request, *args, **kwargs):
        BottomWear = Product.objects.filter(category="BW")
        context = {
            'BottomWear': BottomWear,
        }
        return render(request, 'core/bottom_wear.html', context)




class ProductDetail(DetailView):
    model = Product
    template_name = 'core/productdetail.html'
    # context_object_name = "data"
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


class CustomerRegistration(View):
    def get(self, request):
        form_data = CustomerRegistrationForm()
        return render(request, 'core/customerregistration.html', {'form': form_data})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "you have successfully register!")
            return redirect('login')
        messages.error(request, "try again")
        return render(request, 'core/customerregistration.html', {'form': form})


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


def CustomerLogin(request):
    # CustomerLogin.return_url = request.GET.get('return_url')
    form = LoginForm(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user'] = user.username
            messages.success(request, "you are successfully logging")
            # if CustomerLogin.return_url :
                # return HttpResponseRedirect(CustomerLogin.return_url)
            # else:
            return redirect('profile')
        else:
            if User.objects.filter(Q(username=username) | Q(email=username)).exists():
                messages.error(request, "Please Enter Valid Password ")
            else:
                messages.info(request, "User not found")
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form })

class ChangePassword(PasswordChangeView,View):
    form_class = CustomerPasswordChangeForm
    template_name = 'core/changepassword.html'
    @method_decorator(login_required(login_url='login'))
    def form_valid(self, form):
        form.save()
        messages.success(self.request,'password update successfully! please login again.')
        return redirect('login')


class ResetPassword(PasswordResetView):
    form_class = CustomerPasswordRestForm
    template_name = 'core/resetpassword.html'
    def form_valid(self, form):
        form.save()
        messages.success(self.request,'password reset link shared to your email please check')
        return redirect('home')

# class _CustomerLogin(View):
#     template_name = 'core/login.html'
#
#     def get(self,request):
#         return render(request,'core/login.html',{'form':LoginForm})


def Logout(request):
    logout(request)
    return redirect('home')


class CartView(View):
    @method_decorator(login_required(login_url='login'),name='dispatch')
    def get(self, request):
        products = Cart.objects.filter(user=request.user).order_by('-id')
        if len(products) == 0 :
            return render(request,'core/empty_cart.html')
        else:
            product_count = products.count()
            shipping_charge = 40
            return render(request, 'core/addtocart.html', {'products': products,'shipping_charge':shipping_charge,'product_count':product_count})

    @method_decorator(login_required(login_url='login'),name='dispatch')
    def post(self, request):
        product_id = int(request.POST['product_id'])
        product = Product.objects.get(id=product_id)
        try:
            element = Cart.objects.get(user = request.user,product = product)
            return redirect('cart-view')
        except:
            cart = Cart(user=request.user, product=product)
            cart.save()
            products = Cart.objects.filter(user=request.user).order_by('-id')
            cart_count = products.count()
            request.session['cart_count'] = products.count()
            shipping_charge = 40
            return render(request, 'core/addtocart.html', {'products': products,'shipping_charge':shipping_charge})


def cart_amount(request):
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
    if request.method == 'GET':
        id = request.GET['student_id']
        user = request.user.username
        product = Product.objects.get(id=int(id))
        cart = Cart.objects.get(product=product, user=request.user)
        quantity = cart.quantity
        quantity = quantity + 1
        cart.quantity = quantity
        Cart.save(cart)
        context = {
            'quantity': quantity,
            'cart_amount': cart_amount(request)
        }
        return JsonResponse(context)


def minus_quantity(request):
    if request.method == 'GET':
        id = request.GET['student_id']
        user = request.user.username
        product = Product.objects.get(id=int(id))
        cart = Cart.objects.get(product=product, user=request.user)
        quantity = cart.quantity
        if quantity > 1:
            quantity = quantity - 1
            cart.quantity = quantity
            Cart.save(cart)
        else:
            quantity = quantity
        cart_amount(request)
        context = {
            'quantity': quantity,
            'cart_amount': cart_amount(request)

        }
        return JsonResponse(context)


def remove_item(request):
    if request.method == "GET":
        id = request.GET['item_id']
        Cart.objects.get(id=id).delete()
        cart_count = Cart.objects.filter(user = request.user).count()
        context = {
             'cart_amount': cart_amount(request),
             'cart_count' : cart_count
        }
        return JsonResponse(context)


class Profile(View):
    @method_decorator(login_required(login_url='login'),name='dispatch')

    def get(self,request,*args,**kwargs):
        form = ProfileForm()
        return render(request, 'core/profile.html',{'form': form})
    @method_decorator(login_required(login_url='login'),name='dispatch')
    def post(self,request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username = request.user)
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            obj = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            obj.save()
            messages.success(request, " Address added ")
            try:
                next = request.GET['next']
                return redirect(next)
            except:
                return redirect('address')


class Address(View):
    @method_decorator(login_required(login_url='login'),name='dispatch')

    def get(self,request):
        addresses = Customer.objects.filter(user=request.user)
        return render(request,'core/address.html',{'addresses' : addresses})


class UpdateAddress(UpdateView):
    model = Customer
    form_class = ProfileForm
    template_name = 'core/profile.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    @method_decorator(login_required(login_url='login'),name='dispatch')
    def form_valid(self, form):
        form.save()
        messages.success(self.request,"Address updated")
        return redirect('address')


class DeleteAddress(DeleteView):
    model = Customer
    template_name = 'core/address_delete_confirmation.html'
    success_url = reverse_lazy('address')

#
# def checkout(request):
#     return render(request, 'core/checkout.html')


class OrderSummary(View):
    @method_decorator(login_required(login_url='login'),name='dispatch')
    def get(self,request):
        products = Cart.objects.filter(user= request.user)
        address = Customer.objects.filter(user = request.user)
        try:
            product_id = request.GET['buy_now']
            product = Product.objects.get(id = product_id)
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


class Payment(View):
    @method_decorator(login_required(login_url='login'),name='dispatch')
    def get(self,request):
        try:
            customer_id = request.GET.get('address')
            customer = Customer.objects.get(id = customer_id)

            if self.request.user.is_authenticated:
                products = Cart.objects.filter(user = request.user)
                for product in products:
                    obj = OrderPlaced(user= request.user, customer= customer, product= product.product, quantity= product.quantity )
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
                mail.login(email,password)
                mail.sendmail(email,request.user.email,content)
                mail.close()
                messages.success(request,"Confirmation mail is sended to your Email please check")
                return redirect('orders')
        except:
            messages.warning(request,"please Select Address")
            return redirect('checkout')

        return redirect('login')


class OrdersList(View):
    @method_decorator(login_required(login_url='login'),name='dispatch')
    def get(self,request):
        orders = OrderPlaced.objects.filter(user = request.user).order_by('-id')
        return render(request, 'core/orders.html',{'orders':orders})


class BuyNow(View):
    @method_decorator(login_required(login_url='login'),name='dispatch')

    def get(self,request):
        product_id = request.GET.get('buy_now_product')
        try:
            customer_id = request.GET.get('address')
            product = Product.objects.get(id = product_id)
            customer = Customer.objects.get(id = customer_id)
            if self.request.user.is_authenticated:
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
                mail.login(email,password)
                mail.sendmail(email,request.user.email,content)
                mail.close()
                messages.success(request,"Confirmation mail is sended to your Email please check")
                return redirect('orders')
        except:
            messages.error(request,"Please Select Address")
            return HttpResponseRedirect(f'checkout/?buy_now={product_id}')
        redirect('login')


def search_product(request):
    text = request.GET['search']
    items = Product.objects.filter(title__icontains = text)
    return render(request,'core/search.html',{'items' : items})


