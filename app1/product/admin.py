from django.contrib import admin

# Register your models here.
from product.models import Categories, Subcategories, Products

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Subcategories)
class SubcategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name','quantity','price','category','size']
    list_editable = ['quantity','price','category','size']
    search_fields = ['name']
    list_filter = ['quantity','price','category', ]