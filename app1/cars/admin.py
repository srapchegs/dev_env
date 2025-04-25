from django.contrib import admin

# Register your models here.
from cars.models import Cars

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
