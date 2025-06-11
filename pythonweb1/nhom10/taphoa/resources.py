from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import (
    Product, Categories, Customer, Order, OrderItem,
    News, Review, ShippingAddress, Payment, CartItem
)
from django.contrib.auth.models import User

class CategoriesResource(resources.ModelResource):
    class Meta:
        model = Categories
        # import_id_fields = ['cat_name']  
        fields = ('id', 'cat_name', 'description', 'created_at')


class ProductResource(resources.ModelResource):
    cat_name = fields.Field(
        column_name='categories',         # Tên cột trong Excel
        attribute='cat_name',             # Tên field ForeignKey trong model
        widget=ForeignKeyWidget(Categories, 'cat_name')  # sửa theo đúng tên field bên Categories
    )

    class Meta:
        model = Product
        import_id_fields = ['id']
        fields = ('id', 'created_at', 'product_name', 'description', 'price', 'image', 'categories')


class CustomerResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = Customer
        import_id_fields = ['id']
        fields = ('id', 'user', 'name', 'phone', 'address')


class OrderResource(resources.ModelResource):
    customer = fields.Field(
        column_name='customer',
        attribute='customer',
        widget=ForeignKeyWidget(Customer, 'name')
    )

    class Meta:
        model = Order
        import_id_fields = ['id']
        fields = ('id', 'customer', 'date_ordered', 'complete', 'transaction_id')


class OrderItemResource(resources.ModelResource):
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'product_name')
    )
    order = fields.Field(
        column_name='order',
        attribute='order',
        widget=ForeignKeyWidget(Order, 'id')
    )

    class Meta:
        model = OrderItem
        import_id_fields = ['id']
        fields = ('id', 'product', 'order', 'quantity', 'date_added')


class NewsResource(resources.ModelResource):
    class Meta:
        model = News
        import_id_fields = ['id']
        fields = ('id', 'tieu_de', 'noi_dung', 'ngay_dang', 'trang_thai', 'loai_tin')


class ReviewResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'product_name')
    )

    class Meta:
        model = Review
        import_id_fields = ['id']
        fields = ('id', 'user', 'product', 'rating', 'comment', 'created_at')


class ShippingAddressResource(resources.ModelResource):
    customer = fields.Field(
        column_name='customer',
        attribute='customer',
        widget=ForeignKeyWidget(Customer, 'name')
    )
    order = fields.Field(
        column_name='order',
        attribute='order',
        widget=ForeignKeyWidget(Order, 'id')
    )

    class Meta:
        model = ShippingAddress
        import_id_fields = ['id']
        fields = ('id', 'customer', 'order', 'address', 'date_added')


class PaymentResource(resources.ModelResource):
    order = fields.Field(
        column_name='order',
        attribute='order',
        widget=ForeignKeyWidget(Order, 'id')
    )

    class Meta:
        model = Payment
        import_id_fields = ['id']
        fields = (
            'id', 'order', 'payment_method', 'payment_status',
            'transaction_id', 'paid_amount', 'paid_at'
        )


class CartItemResource(resources.ModelResource):
    customer = fields.Field(
        column_name='customer', 
        attribute='customer',
        widget=ForeignKeyWidget(Customer, 'name')
    )

    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'product_name') 
    )

    class Meta:
        model = CartItem
        import_id_fields = ['id']
        fields = (
            'id', 'customer', 'product', 'quantity', 'create_at'
        )

#  fields.Field: ánh xá order trong payment
# column_name	Tên cột trong file CSV/Excel
# attribute	Tên thuộc tính trong model Django
# widget	(Tùy chọn) Dùng để chuyển đổi dữ liệu – đặc biệt khi là ForeignKey, Date, Boolean, v.v.
#  meta là nơi cấu hình của resource