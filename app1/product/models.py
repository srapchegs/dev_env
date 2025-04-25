from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")

    def __str__(self):
            return self.name
    class Meta:
        db_table = 'category'
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

class Subcategories(models.Model):
    category=models.ForeignKey(to=Categories, on_delete=models.PROTECT, verbose_name="Категория")
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")

    def __str__(self):
                return self.name
    class Meta:
        db_table = 'subcategory'
        verbose_name = "Подкатегорию"
        verbose_name_plural = "Подкатегории"

class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='products_image', verbose_name="Изображение")
    price=models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена")
    compound=models.TextField(verbose_name="Состав")
    size=models.CharField(max_length=150, verbose_name="Размер")
    quantity=models.PositiveIntegerField(default=0, verbose_name="Количество")
    category=models.ForeignKey(to=Subcategories, on_delete=models.PROTECT, verbose_name="Категория")
    
    def __str__(self):
                return self.name    

    class Meta:
        db_table = 'products'
        verbose_name = "Товар"
        verbose_name_plural = "Товары"