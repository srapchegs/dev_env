from django.db import models

# Create your models here.

class Cars(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='car_image', verbose_name="Изображение")
    price=models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена")
    
    def __str__(self):
                return self.name    

    class Meta:
        db_table = 'cars'
        verbose_name = "Спец. технику"
        verbose_name_plural = "Спец. техники"