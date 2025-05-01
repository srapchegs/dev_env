from django.db import models
from users.models import User

# Create your models here.

class Reviews(models.Model):
    review = models.TextField(verbose_name="Отзыв")
    city = models.CharField(max_length=200, verbose_name="Город")
    what_likes = models.TextField(verbose_name="Что понравилось")
    what_modern = models.TextField(verbose_name="Что можно улучшить")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, verbose_name="Пользователь", default=None)

    def __str__(self):
        return f"Отзыв от {self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = 'reviews'
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
