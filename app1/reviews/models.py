from django.db import models

# Create your models here.

class Reviews(models.Model):
    review = models.TextField(verbose_name="Отзыв")
    fio = models.CharField(max_length=200, verbose_name="ФИО")
    city = models.CharField(max_length=200, verbose_name="Город")
    what_likes = models.TextField(verbose_name="Что понравилось")
    what_modern = models.TextField(verbose_name="Что можно улучшить")
    what_modern = models.TextField(verbose_name="Что можно улучшить")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")

    def __str__(self):
        return f"Отзыв от {self.fio}"

    class Meta:
        db_table = 'reviews'
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"