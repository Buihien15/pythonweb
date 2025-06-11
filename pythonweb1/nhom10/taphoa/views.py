from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import datetime
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, StoreReviewForm, NewsSearchForm
from .models import News, Categories, Product, Customer, Order, OrderItem, Review, ShippingAddress, Payment, CartItem, StoreReview
from .utils import cookieCart, cartData, guestOrder, merge_cart

# ViewSets cho API
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CheckoutSerializer
from rest_framework.response import Response
from rest_framework import status
import datetime

class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            customer = request.user.customer
            data = serializer.validated_data

            # Tạo Order
            order = Order.objects.create(
                customer=customer,
                transaction_id=str(datetime.datetime.now().timestamp()),
                complete='hoan_thanh',
            )

            # Tạo OrderItem
            for item in data['items']:
                product = Product.objects.get(id=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity']
                )

            # Tạo địa chỉ giao hàng
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address']
            )

            # Tạo thanh toán
            Payment.objects.create(
                order=order,
                payment_method=data['payment_method'],
                payment_status='success',
                paid_amount=data['total'],
                paid_at=datetime.datetime.now()
            )

            return Response({'message': 'Thanh toán thành công', 'order_id': order.id}, status=201)

        return Response(serializer.errors, status=400)


def base(response):
    """Render sườn chung dành cho các page"""
    return render(response, "main/base.html", {})

def home(response):
    """Render trang home, truyền vào data Product"""
    cartdata = cartData(response)
    cartItems = cartdata['cartItems']

    thucphamkho = Product.objects.filter(cat_name=5)[:8]
    giavisot = Product.objects.filter(cat_name=3)[:8]
    banhkeo = Product.objects.filter(cat_name=6)[:8]
    thucphamanlien = Product.objects.filter(cat_name=4)[:8]
    douong = Product.objects.filter(cat_name=1)[:8]
    sua = Product.objects.filter(cat_name=2)[:8]
    context = {
        'thucphamkho': thucphamkho,
        'cartItems': cartItems,
        'giavisot': giavisot,
        'banhkeo': banhkeo,
        'thucphamanlien': thucphamanlien,
        'douong': douong,
        'sua': sua
    }
    return render(response, "main/home.html", context)

def thucphamkho(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']

    products_list = Product.objects.filter(cat_name=5).order_by('id')
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "main/thucphamkho.html", {'data': page_obj, 'cartItems': cartItems})

def thucphamanlien(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']

    products_list = Product.objects.filter(cat_name=4).order_by('id')  # Sửa cat_name=6 thành 4 (ăn liền)
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "main/thucphamanlien.html", {'data': page_obj, 'cartItems': cartItems})

def giavisot(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']

    products_list = Product.objects.filter(cat_name=3).order_by('id')
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "main/giavisot.html", {'data': page_obj, 'cartItems': cartItems})

def douong(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']

    products_list = Product.objects.filter(cat_name=1).order_by('id')
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "main/douong.html", {'data': page_obj, 'cartItems': cartItems})

def banhkeo(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']

    products_list = Product.objects.filter(cat_name=6).order_by('id')
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "main/banhkeo.html", {'data': page_obj, 'cartItems': cartItems})

def sua(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']

    products_list = Product.objects.filter(cat_name=2).order_by('id')
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "main/sua.html", {'data': page_obj, 'cartItems': cartItems})

def search(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']

    if request.method == "POST":
        searched = request.POST['searched']
        product = Product.objects.filter(product_name__contains=searched).order_by('id')
        return render(request, 'main/search.html', {'searched': searched, 'product': product, 'cartItems': cartItems})
    else:
        return render(request, 'main/search.html', {'cartItems': cartItems})

def update_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            productId = data.get('productId')
            action = data.get('action')
            print('productId:', productId, 'action:', action)

            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

            product = Product.objects.get(id=productId)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

            if action == 'add':
                orderItem.quantity += 1
            elif action == 'remove':
                orderItem.quantity -= 1

            if orderItem.quantity <= 0:
                orderItem.delete()
            else:
                orderItem.save()

            return JsonResponse({'status': 'success', 'message': 'Item updated'})
        except Exception as e:
            print('Error in update_item:', e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def chitietsanpham(request, id):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']
    product_obj = Product.objects.get(id=id)

    related_products_list = Product.objects.filter(cat_name=product_obj.cat_name).exclude(id=product_obj.id).order_by('id')
    paginator = Paginator(related_products_list, 4)
    page_number = request.GET.get('page')
    related_products = paginator.get_page(page_number)

    return render(request, 'main/chitietsanpham.html', {
        'products': product_obj,
        'related_products': related_products,
        'cartItems': cartItems,
    })

def giohang(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']
    items = cartdata['items']
    order = cartdata['order']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'main/giohang.html', context)

@login_required(login_url='/login/')
def thongtinmh(response):
    cartdata = cartData(response)
    cartItems = cartdata['cartItems']
    items = cartdata['items']
    order = cartdata['order']
    user_info = response.user
    customer_info = None
    if user_info.is_authenticated:
        try:
            customer_info = Customer.objects.get(user=user_info)
        except Customer.DoesNotExist:
            customer_info = None
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'user_info': user_info, 'customer_info': customer_info}
    return render(response, 'main/thongtinmh.html', context)

def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'].replace(',', ''))
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address']
    )
    return JsonResponse('Payment submitted..', safe=False)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.get_or_create(
                user=user,
                name=f"{form.cleaned_data['last_name']} {form.cleaned_data['first_name']}",
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin.')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                merge_cart(request, user)
                next_url = request.GET.get('next', 'home')
                response = redirect(next_url)
                response.delete_cookie('cart')
                return response
            else:
                messages.error(request, "Tài khoản hoặc mật khẩu không đúng.")
    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def lienhe(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']
    reviews = StoreReview.objects.order_by('-created_at')

    form = StoreReviewForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = StoreReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.name = request.user.get_full_name() or request.user.username
                review.email = request.user.email
                review.save()
                messages.success(request, 'Cảm ơn bạn đã đánh giá!')
                return redirect('lienhe')
        else:
            messages.warning(request, 'Bạn cần đăng nhập để gửi đánh giá.')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            form = StoreReviewForm(initial={
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email
            })
        else:
            form = StoreReviewForm()

    return render(request, 'main/lienhe.html', {
        'form': form,
        'reviews': reviews,
        'cartItems': cartItems,
    })

def news_list(response):
    cartdata = cartData(response)
    cartItems = cartdata['cartItems']
    loai = response.GET.get('loai')
    if loai in ['khuyen_mai', 'thong_bao']:
        news_list = News.objects.filter(loai_tin=loai, trang_thai=True).order_by('-ngay_dang')
    else:
        news_list = News.objects.filter(trang_thai=True).order_by('-ngay_dang')

    paginator = Paginator(news_list, 5)
    page_number = response.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(response, 'main/news_list.html', {
        'page_obj': page_obj,
        'loai': loai,
        'cartItems': cartItems,
    })

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk, trang_thai=True)
    return render(request, 'main/news_detail.html', {'news_item': news_item})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order, ShippingAddress, Payment

@login_required(login_url='/login/')
def order_history(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer).order_by('-date_ordered')

    order_data = []  # Danh sách chứa tất cả đơn hàng
    for order in orders:
        address = ShippingAddress.objects.filter(order=order).first()
        payment = Payment.objects.filter(order=order).first()
        items = order.orderitem_set.all()

        order_data.append({
            'order': order,
            'items': items,
            'address': address,
            'payment': payment,
        })

    return render(request, 'main/order_history.html', {'order_data': order_data})