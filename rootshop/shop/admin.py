from django.contrib import admin
from .models import Brand, Feature, Car, Customer, CustomerProfile, Order


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year')
    search_fields = ('name', 'country')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'year', 'price', 'is_available')
    list_filter = ('brand', 'transmission', 'is_available')
    search_fields = ('model_name', 'brand__name')
    filter_horizontal = ('features',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'created_at')
    search_fields = ('full_name', 'phone', 'email')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('customer', 'passport_series', 'passport_number', 'address')
    search_fields = ('customer__full_name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'car', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__full_name', 'car__model_name')
