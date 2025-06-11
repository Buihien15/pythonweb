from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
    tieu_de = models.CharField(max_length=200)
    image = models.ImageField(upload_to='NewsImage/', null=True, blank=True)
    noi_dung = models.TextField()
    ngay_dang = models.DateTimeField(auto_now_add=True)
    trang_thai = models.BooleanField(default=True)
    loai_tin = models.CharField(
        max_length=100,
        choices=[('khuyen_mai', 'Khuyến mãi'), ('thong_bao', 'Thông báo')],
        default= 'thong_bao'
    )
    def __str__(self):
        return self.tieu_de
class Categories(models.Model):
    cat_name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    image = models.ImageField(upload_to='product_img/', blank=True, null=True)
    cat_name = models.ForeignKey(Categories, on_delete=models.CASCADE)
  
    stock = models.IntegerField(default=0) # số hàng còn

    def __str__(self):
        return self.product_name

class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    # email = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
	customer = models.ForeignKey(
    Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.CharField(
        max_length=100,
        choices=[('hoan_thanh', 'Hoàn thành'), ('dang_giao', 'Đang giao'), ('dang_chuan_bi_hang', 'Đang chuẩn bị hàng')],
        default= 'dang_chuan_bi_hang'
    )
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
     
     
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.order.id)
    

class CartItem(models.Model):
    """Thông tin giỏ hàng"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
class StoreReview(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}⭐"