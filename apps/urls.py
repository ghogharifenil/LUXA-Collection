from django.urls import path
from . import views

urlpatterns = [
    path('',views.home , name='home'),
    path('collection_department/',views.collection_department , name='collection_department'),

]
