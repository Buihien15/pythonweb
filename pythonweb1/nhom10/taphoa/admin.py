from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
#from . models import News, Categories, Product, Customer, Order, OrderItem, Review, ShippingAddress, Payment 
# Register your models here.
from django.utils.html import format_html
from .models import *
from .resources import (
    CategoriesResource, ProductResource, CustomerResource, OrderResource, OrderItemResource,
    NewsResource, ReviewResource, ShippingAddressResource, PaymentResource,  CartItemResource
)

# from .models import Product
# from .resources import ProductResource



# Cách đăng ký các model để có nút Import/Export
class CategoriesAdmin(ImportExportModelAdmin):
     resource_class = CategoriesResource

class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('product_name', 'cat_name', 'description', 'price', 'image') # Các cột hiển thị trong danh sách Admin
    list_filter = ('cat_name',) # Lọc theo danh mục
    search_fields = ('product_name', 'description') # Tìm kiếm theo tên hoặc mô tả


class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource
    list_display = ('user', 'name', 'phone', 'address') # Các cột hiển thị trong danh sách Admin
    list_filter = ('name', 'phone', 'address',) # Lọc theo danh mục
    search_fields = ('address',)

class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource

class OrderItemAdmin(ImportExportModelAdmin):
    resource_class = OrderItemResource

class NewsAdmin(ImportExportModelAdmin): # Kế thừa từ ImportExportModelAdmin
    resource_class = NewsResource # Gán resource class
    list_display = ('tieu_de', 'loai_tin', 'ngay_dang', 'trang_thai', 'anh')
    list_filter = ('loai_tin', 'trang_thai', 'ngay_dang')
    search_fields = ('tieu_de', 'noi_dung')
    date_hierarchy = 'ngay_dang' # Cho phép lọc theo ngày
    def anh(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="auto" />', obj.image.url)
        return "Không có ảnh"
    
    anh.short_description = 'Anh'

class ReviewAdmin(ImportExportModelAdmin):
    resource_class = ReviewResource

class ShippingAddressAdmin(ImportExportModelAdmin):
    resource_class = ShippingAddressResource
    list_display = ( 'order', 'customer', 'address', 'date_added')
    list_filter = ('customer', 'date_added')
    search_fields = ('address', )

class PaymentAdmin(ImportExportModelAdmin):
    resource_class = PaymentResource

class CartItemAdmin(ImportExportModelAdmin):
    resource_class = CartItemResource

# class CustomerAdmin(ImportExportModelAdmin):
#     pass

# class OrderAdmin(ImportExportModelAdmin):
#     pass

# class OrderItemAdmin(ImportExportModelAdmin):
#     pass

# class NewsAdmin(ImportExportModelAdmin):
#     pass

# class ReviewAdmin(ImportExportModelAdmin):
#     pass

# class ShippingAddressAdmin(ImportExportModelAdmin):
#     pass

# class PaymentAdmin(ImportExportModelAdmin):
#     pass


# Đăng ký các model với các lớp Admin tùy chỉnh
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(StoreReview)



# class NewsAdmin(ImportExportModelAdmin):
#     list_display = ('tieu_de', 'noi_dung', 'ngay_dang', 'trang_thai', 'loai_tin')
# admin.site.register(News, NewsAdmin)

# class CategoriesAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'cat_name', 'description', 'created_at')
# admin.site.register(Categories, CategoriesAdmin)

# class ProductAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'product_name', 'price', 'cat_name', 'created_at')
# admin.site.register(Product, ProductAdmin)

# class CustomerAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'user', 'name', 'email')
# admin.site.register(Customer, CustomerAdmin)

# class OrderAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'customer', 'date_ordered', 'complete', 'transaction_id')
# admin.site.register(Order, OrderAdmin)

# class OrderItemAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'product', 'order', 'quantity', 'date_added')
# admin.site.register(OrderItem, OrderItemAdmin)

# class ReviewAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'user', 'product', 'rating', 'created_at')
# admin.site.register(Review, ReviewAdmin)

# class ShippingAddressAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'customer', 'order', 'address', 'date_added')
# admin.site.register(ShippingAddress, ShippingAddressAdmin)

# class PaymentAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'order', 'payment_method', 'payment_status', 'paid_amount', 'paid_at')
# admin.site.register(Payment, PaymentAdmin)
