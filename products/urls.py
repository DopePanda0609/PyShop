from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new, name='new'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('address/', views.address, name='address'),
]