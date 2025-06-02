import json
from .models import *


def cookieCart(request):
    """tính toán các dữ liệu như là số lượng sản phẩm trong cart, tổng số tiền,..."""
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:

            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'product_name': product.product_name,
                    'price': product.price,
                    'image': product.image
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
                }
            items.append(item)
        except:
            pass

    return{'cartItems':cartItems,'order':order,'items':items}


def cartData(request):
    """Return dữ liệu lấy được từ cookie (người không đăng nhập) trả về cho views.py"""
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except Customer.DoesNotExist:
            # User không có Customer => giỏ rỗng
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = 0
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']

    return{'cartItems':cartItems,'order':order,'items':items}

def guestOrder(request,data):
    """Quy trình order hàng và thu thập dữ liệu lưu vào database"""
    print("User not logged in")
    print("COOKIES:",request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    customer,created = Customer.objects.get_or_create(
            email=email,
            
        )
    customer.name = name
    customer.save()

    order = Order.objects.create(
            customer=customer,
            complete=False,
        )
    for item in items:
            product=Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity'],
            )

    return customer, order