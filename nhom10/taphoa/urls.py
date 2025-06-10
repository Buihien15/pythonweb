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
    path("lienhe/",  views.lienhe, name="lienhe"),

    path("giavisot/",views.giavisot,name="giavisot"),

    # path("giavisot/giavisot-list/<slug:slug>",views.giavisot,name="giavisot"),
    path("thucphamanlien/",views.thucphamanlien,name="thucphamanlien"),
    path("douong/",views.douong,name="douong"),
    path("banhkeo/",views.banhkeo,name="banhkeo"),
    path("sua/",views.sua,name="sua"),
    path("thucphamkho/",views.thucphamkho,name="thucphamkho"),

    # path("kcook/chitietkcook/", views.chitietkcook, name="chitietkcook"),
    path("thongtinmuahang/", views.thongtinmh, name="thongtinmuahang"),
    path('chitietsanpham/<int:id>/', views.chitietsanpham, name='chitietsanpham'),
    path('search/', views.search, name='search'),
    path('update_item/',views.update_item,name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('tin-tuc/', views.news_list, name='news_list'),
    path('tin-tuc/<int:pk>/', views.news_detail, name='news_detail'),

]
 
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  