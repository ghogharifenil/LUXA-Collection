from django.urls import path
from . import views

urlpatterns = [
    path('', views.luxa, name='luxa'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contectus/', views.contectus, name='contectus'),



    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('customerlogout', views.customerlogout, name="customerlogout"),



    path('new_products/', views.new_products, name='new_products'),
    path('collection_department/dress/', views.dress, name='dress'),
    path('collection_department/footwear/', views.footwear, name='footwear'),
    path('collection_department/heals/', views.heals, name='heals'),
    path('collection_department/jwelery/', views.jwelery, name='jwelery'),
    path('collection_department/pent/', views.pent, name='pent'),
    path('collection_department/saree/', views.saree, name='saree'),
    path('collection_department/shert/', views.shert, name='shert'),
    path('collection_department/shoes/', views.shoes, name='shoes'),

    path('search/', views.search_product, name='search_product'),

    path("add-to-cart/<str:product_name>/",views.add_to_cart,name="add_to_cart"),
    path("cart/",views.cart,name="cart"),
    path("increase/<int:cart_id>/",views.increase_qty,name="increase_qty"),
    path("decrease/<int:cart_id>/",views.decrease_qty,name="decrease_qty"),
    path("remove_cart/<int:cart_id>/", views.remove_cart,name="remove_cart"),

    path('checkout/', views.checkout, name='checkout'),


    path('admin/', views.adminuser, name='admin'),
    path('logout/', views.logout, name="logout"),
    path('admin/add_product/', views.add_product, name='add_product'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('order/', views.order, name="order"),
    path('admin/order/ship/<int:order_id>/', views.mark_shipped, name='mark_shipped'),
    path('contact-messages/', views.contact_messages,name='contact_messages'),
    path("resolve-message/<int:id>/",views.resolve_message,name="resolve_message"),

    path('editstock/<str:name>', views.editstock, name="editstock"),
    path('editproduct/<str:name>', views.editproduct, name="editproduct"),
    path("delete_product/<int:product_id>", views.delete_product, name="delete_product"),

    path('admin/admin_dress/', views.admin_dress, name='admin_dress'),
    path('admin/admin_foowear/', views.admin_foowear, name='admin_foowear'),
    path('admin/admin_heels/', views.admin_heels, name='admin_heels'),
    path('admin/admin_jwelery', views.admin_jwelery, name='admin_jwelery'),
    path('admin/admin_pent/', views.admin_pent, name='admin_pent'),
    path('admin/admin_saree/', views.admin_saree, name='admin_saree'),
    path('admin/admin_shert/', views.admin_shert, name='admin_shert'),
    path('admin/admin_shoes/', views.admin_shoes, name='admin_shoes'),


    path('product_detail/<str:name>/', views.detail, name="product_detail"),

]