from django.db import models


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


class ShelvingCategory(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'СтеллажКатегория'
        verbose_name_plural = 'СтеллажКатегории'


class Shelving(models.Model):
    title = models.CharField(max_length=250)
    about = models.TextField()
    Shelvesdepth = models.CharField(max_length=250)
    Dimensions = models.CharField(max_length=250)
    Loadcapacityofeachshelf = models.CharField(max_length=250)
    bracket = models.CharField(max_length=250)
    color = models.CharField(max_length=250)
    img = models.ImageField(upload_to='images/Shelving')
    category = models.ForeignKey(ShelvingCategory, on_delete=models.CASCADE)
    order = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Стеллаж'
        verbose_name_plural = 'Стеллажи'


class ShelvingOrder(models.Model):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    shelving = models.ForeignKey(Shelving, on_delete=models.CASCADE)
    count = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'СтеллажЗаказ'
        verbose_name_plural = 'СтеллажЗаказы'


class ShelvingGallery(models.Model):
    img = models.ImageField(upload_to='images/Shelving')
    shelving = models.ForeignKey(Shelving, on_delete=models.CASCADE, related_name='gallery')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.img.url)

    class Meta:
        verbose_name = 'СтеллажГалерея'
        verbose_name_plural = 'СтеллажГалереи'


class CategoryProduct(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'КатегорияПродукта'
        verbose_name_plural = 'КатегорииПродуктов'


class Product(models.Model):
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    image = models.ImageField(upload_to='products/')
    full_description = models.TextField()
    work_zone_length = models.CharField(max_length=50, verbose_name="Длина рабочей зоны")
    floor_zone_length = models.CharField(max_length=50, verbose_name="Длина напольной зоны")
    width = models.CharField(max_length=50, verbose_name="Ширина")
    height = models.CharField(max_length=50, verbose_name="Высота")
    work_zone_width = models.CharField(max_length=50, verbose_name="Ширина рабочей зоны")
    working_surface = models.CharField(max_length=100, verbose_name="Рабочая поверхность")
    coating = models.CharField(max_length=100, verbose_name="Покрытие")
    color = models.CharField(max_length=100, verbose_name="Цвет")
    protective_bumper = models.CharField(max_length=100, verbose_name="Защитный бампер")
    contact = models.CharField(max_length=100, verbose_name="Контакты")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


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
        verbose_name = 'ЗаказПродукта'
        verbose_name_plural = 'ЗаказыПродуктов'


class Promotion(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название акции")
    description = models.TextField(verbose_name="Описание акции")
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2,
                                              verbose_name="Скидка (%)")
    products = models.ManyToManyField('Product', related_name='promotions', blank=True, verbose_name="Продукты")
    shelvings = models.ManyToManyField('Shelving', related_name='promotions', blank=True, verbose_name="Стеллажи")

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
    shelvings = models.ManyToManyField('Shelving', related_name='projects', blank=True, verbose_name="Стеллажи")
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
