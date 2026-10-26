from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class Brand(models.Model):
    """Марка автомобиля (один ко многим с Car)."""
    name = models.CharField('Название', max_length=100, unique=True)
    country = models.CharField('Страна', max_length=100)
    founded_year = models.PositiveIntegerField(
        'Год основания',
        null=True,
        blank=True,
        validators=[MinValueValidator(1880), MaxValueValidator(2030)],
    )
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'
        ordering = ['name']

    def __str__(self):
        return self.name


class Feature(models.Model):
    """Опция / комплектация (многие ко многим с Car)."""
    name = models.CharField('Название', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'
        ordering = ['name']

    def __str__(self):
        return self.name


class Car(models.Model):
    """Автомобиль."""
    TRANSMISSION_CHOICES = [
        ('AT', 'Автомат'),
        ('MT', 'Механика'),
        ('CVT', 'Вариатор'),
        ('DCT', 'Робот'),
    ]
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Марка',
    )
    model_name = models.CharField('Модель', max_length=100)
    year = models.PositiveIntegerField(
        'Год выпуска',
        validators=[MinValueValidator(1990), MaxValueValidator(2030)],
    )
    price = models.DecimalField(
        'Цена, ₽',
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(100000)],
    )
    mileage = models.PositiveIntegerField('Пробег, км', default=0)
    transmission = models.CharField(
        'КПП',
        max_length=3,
        choices=TRANSMISSION_CHOICES,
        default='AT',
    )
    engine = models.CharField('Двигатель', max_length=100, blank=True)
    features = models.ManyToManyField(
        Feature,
        related_name='cars',
        blank=True,
        verbose_name='Опции',
    )
    is_available = models.BooleanField('В наличии', default=True)
    created_at = models.DateTimeField('Добавлен', auto_now_add=True)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.brand} {self.model_name} ({self.year})'


class Customer(models.Model):
    """Клиент."""
    phone_validator = RegexValidator(
        regex=r'^\+?[0-9]{10,15}$',
        message='Телефон в формате +7XXXXXXXXXX или 10–15 цифр',
    )
    full_name = models.CharField('ФИО', max_length=150)
    phone = models.CharField('Телефон', max_length=20, validators=[phone_validator])
    email = models.EmailField('Email', blank=True)
    created_at = models.DateTimeField('Зарегистрирован', auto_now_add=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class CustomerProfile(models.Model):
    """Профиль клиента (один к одному с Customer)."""
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Клиент',
    )
    passport_series = models.CharField(
        'Серия паспорта',
        max_length=10,
        blank=True,
        validators=[RegexValidator(r'^\d{4}$', 'Серия — 4 цифры')],
    )
    passport_number = models.CharField(
        'Номер паспорта',
        max_length=20,
        blank=True,
        validators=[RegexValidator(r'^\d{6}$', 'Номер — 6 цифр')],
    )
    address = models.CharField('Адрес', max_length=255, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = 'Профиль клиента'
        verbose_name_plural = 'Профили клиентов'

    def __str__(self):
        return f'Профиль: {self.customer.full_name}'


class Order(models.Model):
    """Заказ (один ко многим: клиент → заказы, авто → заказы)."""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('paid', 'Оплачен'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Клиент',
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Автомобиль',
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
    )
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Дата заказа', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.pk}: {self.customer} → {self.car}'
