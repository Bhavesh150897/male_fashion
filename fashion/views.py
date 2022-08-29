from django.shortcuts import render, get_object_or_404
from django import template
from django.db.models import Min,Max
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.template import loader
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate,get_user_model
from django.contrib.auth import login as auth_login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegisterForm, LoginForm, CustomerProfileForm
from django.views import View
from .models import Slider, Product,Catagory, Cart, FavouriteProduct, Customer, OrderPlaced, Variation, Size, Color, Brand
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView,TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import razorpay

# Create your views here.
class ProductView(View):
    def get(self, request):
        sliders = Slider.objects.all()
        products_trending = Product.objects.filter(trending=1)[0]
        products_seller = Product.objects.filter(label='Best Seller')
        products_new = Product.objects.filter(label='New')
        products_sale = Product.objects.filter(label='Sale')
        return render(request, 'fashion/home.html',{ 'sliders': sliders,'products_seller':products_seller,'products_new':products_new,'products_sale':products_sale,'products_trending':products_trending })

def about(request):
    return render(request, 'fashion/about.html')    

def shop(request):
    totalitem = 0
    amount = 0
    shipping_amount = 70.0
    totalamount = 0
    products = Product.objects.all()
    productCount = Product.objects.count()
    catagories = Catagory.objects.all()
    brands = Brand.objects.all()
    minMaxPrice=Product.objects.aggregate(Min('original_price'),Max('original_price'))
    order_by = request.GET.get('order_by', None)
    
    if order_by == 'highest':
        products = Product.objects.order_by('-original_price')

    else:
        products = Product.objects.order_by('original_price')

    page = request.GET.get('page', 1)

    paginator = Paginator(products, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount+shipping_amount
    return render(request, 'fashion/shop.html',{ 'products': products ,'catagories':catagories,'totalitem':totalitem,'totalamount':totalamount,'brands':brands,'productCount':productCount,'minMaxPrice':minMaxPrice}) 

def contact(request):
    return render(request, 'fashion/contact.html')

def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    item_already_in_cart1 = False
    product = request.GET.get('prod_id')
    item_already_in_cart1 = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
    if item_already_in_cart1 == False:
        product_title = Product.objects.get(id=product)
        Cart(user=user, product=product_title).save()
        messages.success(request, 'Product add to cart successfully!')
        return redirect('/cart')
    else:
        messages.success(request, 'Product add to cart successfully!')
        return redirect('/cart')

def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount=0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.original_price)
                amount += tempamount
            totalamount = amount+shipping_amount
            return render(request, 'fashion/cart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem})
        else:
            return render(request, 'fashion/emptycart.html', {'totalitem':totalitem})
    else:
        return render(request, 'fashion/emptycart.html', {'totalitem':totalitem})

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount= 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.original_price)
            amount += tempamount
        data = {
            'prod_id':prod_id,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount= 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.original_price)
            amount += tempamount
        data = {
            'prod_id':prod_id,
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount= 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.original_price)
            amount += tempamount
        data = {
            'prod_id':prod_id,
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")

def Favorites(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    Favourites,_ = FavouriteProduct.objects.get_or_create(user=user)

    product = Product.objects.get(id=id)

    if product not in Favourites.product.all():
        Favourites.product.add(product)
        data = {
            'product':True
        }
        return JsonResponse(data)
    else:
        Favourites.product.remove(product)
    
    Favourites.save()
    return HttpResponse('Success')

def favoritesPage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    FavProducts,_ = FavouriteProduct.objects.get_or_create(user=user)
    return render(request, 'fashion/favourites.html', { 'product_list': FavProducts.product.all(), "favorites": True})

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.original_price)
            amount += tempamount
        totalamount = amount+shipping_amount
        
        response_payment = ''
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        response_payment = client.order.create(dict(amount=int(totalamount*100),
                                                    currency='USD')
                                               )
        order_id = response_payment['id']
        order_status = response_payment['status']
        
        if order_status == 'created':
            order = OrderPlaced(
                amount=totalamount,
                order_id=order_id,
                user_id=request.user.id,
                product_id=p.product.id,
                customer_id=p.product.customer.id,
            )
            order.save()
            response_payment['email'] = request.user.email

    return render(request, 'fashion/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount,'payment':response_payment})

@csrf_exempt
def payment_status(request):
    response = request.POST
    print(response)
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    # client instance
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        order = OrderPlaced.objects.get(order_id=response['razorpay_order_id'])
        order.razorpay_payment_id = response['razorpay_payment_id']
        order.has_paid = True
        order.save()
        return render(request, 'fashion/callback.html', {'status': True})
    except:
        return render(request, 'fashion/callback.html', {'status': False})


class productDetails(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        size = Size.objects.all()
        color = Color.objects.all()
        products = Product.objects.filter(category_id=product.category_id)
        product_in_favorites = None
        item_already_in_cart=False
        if request.user.is_authenticated:

            Favourites,_ = FavouriteProduct.objects.get_or_create(user=request.user)

            if product in Favourites.product.all():
                product_in_favorites = True
            else:
                product_in_favorites = False


        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'fashion/proDetails.html', {'product':product,'totalitem':totalitem,'product_in_favorites':product_in_favorites,'item_already_in_cart':item_already_in_cart,'products':products,'stripe_publishable_key':settings.STRIPE_PUBLISHABLE_KEY,'size':size,'color':color})

class CustomerView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'fashion/userProfile.html', {'form':form,'active':'active'})
  
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            if profile.user_id is None:
                profile.user_id = request.user.id
            profile.save()
            messages.success(request, 'Congratulations!! Registered Successfully.')
        return render(request, 'fashion/userProfile.html', {'form':form})

def address(request):
    if not request.user.is_authenticated:
        return redirect('login')

    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'fashion/address.html',{'add':add,'active':'active'})

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'fashion/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(email=email, password=raw_password)

            messages.success(request, 'User created Successfully!')
            return redirect('login')
        else:
            messages.warning(request, 'Oops! something went wrong!')

        return render(request, self.template_name, {'form': form})

def login(request):
    form = LoginForm(request.POST or None)

    if not request.user.is_authenticated:
        if request.method == "POST":

            if form.is_valid():
                user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'You have successfully login!')
                    return redirect('home')
                else:
                    messages.warning(request, 'Invalid credentials!')
            else:
                messages.warning(request, 'Oops! something went wrong!')
        return render(request, "fashion/login.html", {"form": form})
    return redirect("login")

def search(request):
    query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', None)
    
    if order_by == 'highest':
        products=Product.objects.filter(Q(name__icontains=query)).order_by('-original_price')
    else:
        products=Product.objects.filter(Q(name__icontains=query)).order_by('original_price')

    page = request.GET.get('page', 1)

    paginator = Paginator(products, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    catagories = Catagory.objects.all()
    params={'product_list':products,'catagories':catagories}
    return render(request,'fashion/search.html',params)

def product_cat(request,slug):
    category = Catagory.objects.filter(slug=slug).first()
    products = Product.objects.filter(category_id=category.id)
    brands = Brand.objects.all()

    order_by = request.GET.get('order_by', None)
    
    if order_by == 'highest':
        products = Product.objects.filter(category_id=category.id).order_by('-original_price')
    else:
        products = Product.objects.filter(category_id=category.id).order_by('original_price')

    page = request.GET.get('page', 1)

    paginator = Paginator(products, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    catagories = Catagory.objects.all()
    template = loader.get_template('fashion/productCat.html')
    context = {
        'products': products,
        'category': category,
        'slug': slug,
        'catagories': catagories,
        'brands': brands,
    }
    return HttpResponse(template.render(context, request))

def brand_cat(request,slug):
    brand = Brand.objects.filter(slug=slug).first()
    products = Product.objects.filter(brand_id=brand.id)

    order_by = request.GET.get('order_by', None)
    
    if order_by == 'highest':
        products = Product.objects.filter(brand_id=brand.id).order_by('-original_price')
    else:
        products = Product.objects.filter(brand_id=brand.id).order_by('original_price')

    page = request.GET.get('page', 1)

    paginator = Paginator(products, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    catagories = Catagory.objects.all()
    brands = Brand.objects.all()
    template = loader.get_template('fashion/brandCat.html')
    context = {
        'products': products,
        'brand': brand,
        'brands': brands,
        'slug': slug,
        'catagories': catagories,
    }
    return HttpResponse(template.render(context, request))

# Filter Data
def filter_data(request):
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    allProducts=Product.objects.all().order_by('-id').distinct()
    allProducts=allProducts.filter(original_price__gte=minPrice)
    allProducts=allProducts.filter(original_price__lte=maxPrice)
    print(allProducts)
    t=render_to_string('fashion/product-list.html',{'data':allProducts})
    return JsonResponse({'data':t})