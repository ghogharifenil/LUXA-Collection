from django.urls import path
from . import views

urlpatterns = [
    path('', views.luxa, name='luxa'),
    path('home/', views.home, name='home'),


    path('collection_department/', views.collection_department,
         name='collection_department'),

    path('collection_department/dress/', views.dress, name='dress'),
    path('collection_department/footwear/', views.footwear, name='footwear'),
    path('collection_department/heals/', views.heals, name='heals'),
    path('collection_department/jwelery/', views.jwelery, name='jwelery'),
    path('collection_department/pent/', views.pent, name='pent'),
    path('collection_department/saree/', views.saree, name='saree'),
    path('collection_department/shert/', views.shert, name='shert'),
    path('collection_department/shoes/', views.shoes, name='shoes'),


    path('buy/<str:name>', views.buy, name="buy"),


    path('admin/', views.adminuser, name='admin'),
    path('logout/', views.logout, name="logout"),
    path('admin/add_product/', views.add_product, name='add_product'),
    path('admin/viewpro', views.viewpro, name='view_product'),
    path('dashboard/', views.dashboard, name="dashboard"),

    path('editstock/<str:name>', views.editstock, name="editstock"),
    path('editproduct/<str:name>', views.editproduct, name="editproduct"),


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
