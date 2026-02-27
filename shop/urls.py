from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('order/<int:pizza_id>/', views.order_pizza, name='order_pizza'),

    
]
