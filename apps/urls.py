from django.urls import path
from . import views

urlpatterns = [
    path('',views.luxa, name='luxa'),
    path('home/',views.home, name='home'),
    path('collection_department/',views.collection_department , name='collection_department'),
    path('collection_department/dress/',views.dress, name='dress'),
    path('collection_department/footwear/',views.footwear, name='footwear'),
    path('collection_department/heals/',views.heals, name='heals'),
    path('collection_department/jwelery/',views.jwelery, name='jwelery'),
    path('collection_department/pent/',views.pent, name='pent'),
    path('collection_department/saree/',views.saree, name='saree'),
    path('collection_department/shert/',views.shert, name='shert'),
    path('collection_department/shoes/',views.shoes, name='shoes'),
    path('add_product/',views.add_product, name='add_product'),



]
