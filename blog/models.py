from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название Категории")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="Родительская Категория"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    full_description = RichTextField()
    image = models.ImageField(upload_to='products/')
    contact = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class OrderProduct(models.Model):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    count = models.CharField(max_length=250)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заказ Продукта'
        verbose_name_plural = 'Заказы Продуктов'


class Promotion(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название акции")
    description = models.TextField(verbose_name="Описание акции")
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2,
                                              verbose_name="Скидка (%)", null=True, blank=True)
    products = models.ManyToManyField('Product', related_name='promotions', blank=True, verbose_name="Продукты")

    def __str__(self):
        return f"{self.title} - {self.discount_percentage}%"

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


class Project(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание проекта")
    image = models.ImageField(upload_to='projects/', verbose_name="Изображение проекта")
    products = models.ManyToManyField('Product', related_name='projects', blank=True, verbose_name="Продукты")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ваше имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    interested_product = models.CharField(max_length=255, verbose_name="Интересующая продукция")
    message = models.TextField(verbose_name="Сообщение")
    attached_file = models.FileField(upload_to='inquiries/', blank=True, null=True, verbose_name="Прикрепить файл")
    consent = models.BooleanField(default=False, verbose_name="Согласен на обработку персональных данных")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = 'ЗапросКонтакта'
        verbose_name_plural = 'ЗапросыКонтактов'
