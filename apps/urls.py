from django.urls import path
from . import views

urlpatterns = [
    path('',views.luxa, name='luxa'),
    path('home/',views.home, name='home'),
    path('collection_department/',views.collection_department , name='collection_department'),

]
