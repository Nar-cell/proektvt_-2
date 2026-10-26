from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Brand, Feature, Car, Customer, CustomerProfile, Order
from .forms import (
    BrandForm, FeatureForm, CarForm,
    CustomerForm, CustomerProfileForm, OrderForm,
)


def main(request):
    return render(request, 'main.html')


def about(request):
    return render(request, 'about.html')


def catalog(request):
    return render(request, 'catalog.html')


def brand_page(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Марка успешно добавлена.')
            return redirect('brands')
    else:
        form = BrandForm()
    items = Brand.objects.all()
    return render(request, 'crud/brands.html', {'form': form, 'items': items})


def feature_page(request):
    if request.method == 'POST':
        form = FeatureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Опция успешно добавлена.')
            return redirect('features')
    else:
        form = FeatureForm()
    items = Feature.objects.all()
    return render(request, 'crud/features.html', {'form': form, 'items': items})


def car_page(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Автомобиль успешно добавлен.')
            return redirect('cars')
    else:
        form = CarForm()
    items = Car.objects.select_related('brand').prefetch_related('features').all()
    return render(request, 'crud/cars.html', {'form': form, 'items': items})


def customer_page(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клиент успешно добавлен.')
            return redirect('customers')
    else:
        form = CustomerForm()
    items = Customer.objects.all()
    return render(request, 'crud/customers.html', {'form': form, 'items': items})


def profile_page(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль клиента успешно добавлен.')
            return redirect('profiles')
    else:
        form = CustomerProfileForm()
    items = CustomerProfile.objects.select_related('customer').all()
    return render(request, 'crud/profiles.html', {'form': form, 'items': items})


def order_page(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ успешно создан.')
            return redirect('orders')
    else:
        form = OrderForm()
    items = Order.objects.select_related('customer', 'car', 'car__brand').all()
    return render(request, 'crud/orders.html', {'form': form, 'items': items})
