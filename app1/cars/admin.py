from django.contrib import admin

# Register your models here.
from cars.models import Cars, CarsBid


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(CarsBid)