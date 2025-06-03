from django.urls import path
from django.conf import settings  
from django.conf.urls.static import static  
from . import views
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
    path("rongbien/",views.rongbien,name="rongbien"),

    # path("kcook/chitietkcook/", views.chitietkcook, name="chitietkcook"),
    path("thongtinmuahang/", views.thongtinmh, name="thongtinmuahang"),
    path('chitietsanpham/<int:id>/', views.chitietsanpham, name='chitietsanpham'),
    path('search/', views.search, name='search'),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),


]
 
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  