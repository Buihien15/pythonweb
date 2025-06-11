from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from.views import CheckoutAPIView

'''Thiết lập các đường dẫn đến các trang cụ thể'''
urlpatterns = [
    # path("<int:id>",views.index,name="index"),
    path("",views.home,name="home"),
    path("home/",views.home,name="home"),
    path("giohang/",views.giohang,name="giohang"),

    path("giavisot/",views.giavisot,name="giavisot"),

    # path("giavisot/giavisot-list/<slug:slug>",views.giavisot,name="giavisot"),
    path("thucphamanlien/",views.thucphamanlien,name="thucphamanlien"),
    path("douong/",views.douong,name="douong"),
    path("banhkeo/",views.banhkeo,name="banhkeo"),
    path("sua/",views.sua,name="sua"),
    path("thucphamkho/",views.thucphamkho,name="thucphamkho"),

    # path("kcook/chitietkcook/", views.chitietkcook, name="chitietkcook"),
    path('thongtinmuahang/', views.thongtinmh, name='thongtinmuahang'),
    path('chitietsanpham/<int:id>/', views.chitietsanpham, name='chitietsanpham'),
    path('search/', views.search, name='search'),
    path('update_item/',views.update_item,name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("lienhe/",  views.lienhe, name="lienhe"),
    path('tin-tuc/', views.news_list, name='news_list'),
    path('tin-tuc/<int:pk>/', views.news_detail, name='news_detail'),
    #api
    path('lich-su-don-hang/', views.order_history, name='order_history'),
    path('api/checkout/', CheckoutAPIView.as_view(), name='checkout'),
  
]
 
