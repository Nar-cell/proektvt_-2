from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('catalog/', views.catalog, name='catalog'),
    path('about/', views.about, name='about'),
    # CRUD pages
    path('brands/', views.brand_page, name='brands'),
    path('features/', views.feature_page, name='features'),
    path('cars/', views.car_page, name='cars'),
    path('customers/', views.customer_page, name='customers'),
    path('profiles/', views.profile_page, name='profiles'),
    path('orders/', views.order_page, name='orders'),
]
