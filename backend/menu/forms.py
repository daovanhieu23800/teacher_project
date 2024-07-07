from django import forms

from .models import Ingredient, Dish


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name']


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description']
