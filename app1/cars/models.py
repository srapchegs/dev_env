from django.db import models
from users.models import User


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
    
class CarsBid(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, verbose_name="Пользователь", default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки заявки")
    cars = models.ForeignKey(to=Cars, on_delete=models.SET_DEFAULT, verbose_name="Машина", default=None)
    bid_address = models.TextField(verbose_name="Адрес заявки")
    date_rent = models.TextField(verbose_name="Даты и сроки аренды")

    class Meta:
        db_table = "car_bid"
        verbose_name = "Заявку"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"Заявка на {self.cars.name} | Заявитель {self.user.first_name} {self.user.last_name}"
