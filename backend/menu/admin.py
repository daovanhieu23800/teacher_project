from django.contrib import admin

# Register your models here.
from .models import Dish, DishIngredient, Ingredient

admin.site.register(Dish)
admin.site.register(DishIngredient)
admin.site.register(Ingredient)
