from multiprocessing import context
from queue import PriorityQueue
from sqlite3 import Cursor
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Customer, Product, Order, OrderItem,ShippingAddress
from django.http import JsonResponse
import json
from .utils import cookieCart,cartData,guestOrder
import datetime
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

# def index(response,id):
#     ls = ToDoList.objects.get(id = id)
#     # {"save":["save"], "c1":["clicked"]}
#     if response.method == "POST":
#         print(response.POST)
#         if response.POST.get("save"):
#             for item in ls.item_set.all():
#                 if response.POST.get(("c"+str(item.id)) == "clicked"):

#                     item.complete = True
#                 else:
#                     item.complete = False

#                 item.save()


#         elif response.POST.get("newItem"):
#             txt = response.POST.get("new")
#             if len(txt) >2 :
#                 ls.item_set.create(text = txt,complete = False)
#             else:
#                 print("invalid Input")

#     return render (response,"main/list.html",{"ls":ls})


# def home(response):
#     data = Product.objects.filter(pk__in = [14,15,16,19,18,22,27,28,29,24,25,30,10,11,13])

#     return render (response,"main/home.html",{'data':data})

# def create(response):
#     if response.method == "POST":
#         form = CreateNewList(response.POST)
#         if form.is_valid():
#             n=form.cleaned_data["name"]
#             t= ToDoList(name=n)
#             t.save()

#         return HttpResponseRedirect("/%i" %t.id)

#     else:
#         form = CreateNewList()
#     return render(response,"main/create.html",{"form":form})

# def giohang(response):
#     return render(response,"main/giohang.html",{})



def base(response):
    """render sườn chung dành cho các page"""
    return render(response, "main/base.html", {})


def home(response):
    """render trang home, truyền vào data Product"""
    cartdata=cartData(response)
    cartItems = cartdata['cartItems']
    
    thucphamkho = Product.objects.filter(cat_name = 5)[:8]
    giavisot = Product.objects.filter(cat_name = 3)[:8]
    banhkeo = Product.objects.filter(cat_name = 6)[:8]
    thucphamanlien = Product.objects.filter(cat_name = 4)[:8]
    douong = Product.objects.filter(cat_name = 1)[:8] 
    sua = Product.objects.filter(cat_name = 2)[:8]
    context = {'thucphamkho': thucphamkho, 'cartItems': cartItems,'giavisot':giavisot,'banhkeo':banhkeo,'thucphamanlien':thucphamanlien,'douong':douong,'sua':sua}

    return render(response, "main/home.html",context)

def thucphamkho(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']

    products_list = Product.objects.filter(cat_name=5).order_by('id')  # cat_name=5 là thực phẩm khô
    paginator = Paginator(products_list, 12)  # 12 sản phẩm mỗi trang

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "main/thucphamkho.html", {
        'data': page_obj,
        'cartItems': cartItems,
    })

def thucphamanlien(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']

    products_list = Product.objects.filter(cat_name=6).order_by('id')  # cat_name=6 là thực phẩm ăn liền
    paginator = Paginator(products_list, 12)  # Hiển thị 12 sản phẩm mỗi trang

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "main/thucphamanlien.html", {
        'data': page_obj,
        'cartItems': cartItems,
    })

def giavisot(request):
    cartdata = cartData(request)
    cartItems = cartdata['cartItems']

    products_list = Product.objects.filter(cat_name=3).order_by('id')
    paginator = Paginator(products_list, 12)  # 12 sản phẩm mỗi trang

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "main/giavisot.html", {
        'data': page_obj,
        'cartItems': cartItems,
    })

def douong(request):
    """render trang đồ uống, truyền vào data là Product với CategoryId=4 (vì id=4 là đồ uống)"""
    cartdata=cartData(request)
    cartItems = cartdata['cartItems']
    products_list = Product.objects.filter(cat_name=1).order_by('id')
    paginator = Paginator(products_list, 12)  # 12 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "main/douong.html", {
        'data': page_obj,
        'cartItems': cartItems,
    })
    


def banhkeo(request):
    """render trang bánh kẹo, truyền vào data là Product với CategoryId=1 (vì id=1 là bánh kẹo)"""
    cartdata=cartData(request)
    cartItems = cartdata['cartItems']
    products_list = Product.objects.filter(cat_name=6).order_by('id')
    paginator = Paginator(products_list, 12)  # 12 sản phẩm mỗi trang
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, "main/banhkeo.html", {
        'data': page_obj,
        'cartItems': cartItems,
    })


def sua(request):
    """render trang rong biển, truyền vào data là Product với CategoryId=5 (vì id=5 là rong biển)"""
    cartdata=cartData(request)
    cartItems = cartdata['cartItems']
    products_list = Product.objects.filter(cat_name=2).order_by('id')
    paginator = Paginator(products_list, 12)  # 12 sản phẩm mỗi trang
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, "main/sua.html", {
        'data': page_obj,
        'cartItems': cartItems,
    })



def search(request):
    """render trang search, trang này sẽ hiện kết quả khi người dùng nhập từ khóa vào ô search"""
    cartdata=cartData(request)
    cartItems = cartdata['cartItems']

    if request.method == "POST":
        searched = request.POST['searched']
        product = Product.objects.filter(product_name__contains=searched)
        return render(request, 'main/search.html', {'searched': searched, 'product': product,'cartItems':cartItems})
    else:
        return render(request, 'main/search.html', {'cartItems':cartItems})


from django.http import JsonResponse
import json

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
    # Lấy sản phẩm theo id
    cartdata=cartData(request)
    cartItems = cartdata['cartItems']
    product_obj = Product.objects.get(id=id)

    # Lấy sản phẩm liên quan (cùng category, loại trừ sản phẩm đang xem)
    related_products_list = Product.objects.filter(
        cat_name=product_obj.cat_name
    ).exclude(id=product_obj.id).order_by('id')

    paginator = Paginator(related_products_list, 4)  # 5 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    related_products = paginator.get_page(page_number)

    return render(request, 'main/chitietsanpham.html', {
        'products': product_obj,
        'related_products': related_products,
        'cartItems': cartItems,
    })
    
def giohang(request):
    """render trang giỏ hàng"""
    cartdata=cartData(request)
    cartItems = cartdata['cartItems']
    items = cartdata['items']
    order= cartdata['order']


    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'main/giohang.html', context)


def thongtinmh(response):
    """render trang thông tin mua hàng"""
    cartdata=cartData(response)
    cartItems = cartdata['cartItems']
    items = cartdata['items']
    order= cartdata['order']

    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(response, 'main/thongtinmh.html', context)

def processOrder(request):
    """Quy trình order hàng và thu thập dữ liệu lưu vào database"""
    print('Data:',request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
       
    else:
        customer,order = guestOrder(request,data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True

    order.save()

    ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address = data['shipping']['address']
        )
    return JsonResponse('Payment submitted..', safe=False)