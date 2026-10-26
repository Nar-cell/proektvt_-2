from django import forms
from django.core.exceptions import ValidationError
from .models import Brand, Feature, Car, Customer, CustomerProfile, Order


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'country', 'founded_year', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Например, BMW'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Германия'}),
            'founded_year': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '1916'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise ValidationError('Название марки должно содержать минимум 2 символа.')
        qs = Brand.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError(f'Марка «{name}» уже существует.')
        return name

    def clean_founded_year(self):
        year = self.cleaned_data.get('founded_year')
        if year is not None and (year < 1880 or year > 2030):
            raise ValidationError('Год основания должен быть между 1880 и 2030.')
        return year


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Кожаный салон'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise ValidationError('Название опции слишком короткое.')
        return name


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand', 'model_name', 'year', 'price', 'mileage',
            'transmission', 'engine', 'features', 'is_available',
        ]
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-input'}),
            'model_name': forms.TextInput(attrs={'class': 'form-input'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': 1000}),
            'mileage': forms.NumberInput(attrs={'class': 'form-input'}),
            'transmission': forms.Select(attrs={'class': 'form-input'}),
            'engine': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '2.0 л · 197 л.с.'}),
            'features': forms.CheckboxSelectMultiple(),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 100000:
            raise ValidationError('Цена не может быть меньше 100 000 ₽.')
        return price

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year is not None and (year < 1990 or year > 2030):
            raise ValidationError('Год выпуска должен быть в диапазоне 1990–2030.')
        return year

    def clean(self):
        cleaned = super().clean()
        year = cleaned.get('year')
        mileage = cleaned.get('mileage')
        if year and mileage is not None:
            if year >= 2024 and mileage > 5000:
                raise ValidationError('У нового автомобиля (2024+) пробег обычно не превышает 5000 км. Проверьте данные.')
        return cleaned


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иванов Иван Иванович'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+79001234567'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'mail@example.com'}),
        }

    def clean_full_name(self):
        name = self.cleaned_data['full_name'].strip()
        parts = name.split()
        if len(parts) < 2:
            raise ValidationError('Укажите хотя бы фамилию и имя.')
        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip().replace(' ', '').replace('-', '')
        if not phone.startswith('+') and phone.isdigit() and len(phone) == 11 and phone.startswith('8'):
            phone = '+7' + phone[1:]
        return phone


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['customer', 'passport_series', 'passport_number', 'address', 'birth_date', 'notes']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-input'}),
            'passport_series': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '1234'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '567890'}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }

    def clean(self):
        cleaned = super().clean()
        series = cleaned.get('passport_series') or ''
        number = cleaned.get('passport_number') or ''
        if (series and not number) or (number and not series):
            raise ValidationError('Укажите и серию, и номер паспорта вместе, либо оставьте оба поля пустыми.')
        return cleaned


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'car', 'status', 'comment']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-input'}),
            'car': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }

    def clean_car(self):
        car = self.cleaned_data.get('car')
        if car and not car.is_available:
            raise ValidationError(f'Автомобиль «{car}» сейчас недоступен для заказа.')
        return car
