from django.shortcuts import render, redirect
from .models import Dish, Ingredient, DishIngredient
from django.http import JsonResponse, HttpResponse
import json
import csv
# Create your views here.


def index(request):
    dishes = Dish.objects.all()
    ingredients = Ingredient.objects.all()
    dish_ingredients = DishIngredient.objects.all()
    return render(request, 'menu/index.html', {
        'dishes': dishes,
        'ingredients': ingredients,
        'dish_ingredients': dish_ingredients,
    })


def ingredient(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        ingredients_list = list(ingredients.values())
        return JsonResponse({'ingredients': ingredients_list})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if name is not None:
                Ingredient.objects.create(name=name)
                return JsonResponse({'message': 'Ingredient added successfully!'}, status=201)
            else:
                return JsonResponse({'error': 'Name are required.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            name = data.get('name')

            if name:
                try:
                    ingredient = Ingredient.objects.get(name=name)
                    dish_ngredient = DishIngredient.objects.filter(
                        ingredient=ingredient).exists()
                    if dish_ngredient:
                        return JsonResponse({'message': f'ingredient is belong to some dish '}, status=404)
                    ingredient.delete()
                    return JsonResponse({'message': f'ingredient deleted successful '}, status=200)
                except Ingredient.DoesNotExist:
                    return JsonResponse({'error': 'ingredient does not exist.'}, status=404)
            else:
                return JsonResponse({'error': 'Ingredient Name is required.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)


def dish(request):
    if request.method == 'GET':
        dishes = Dish.objects.all()
        dishes_list = list(dishes.values())
        return JsonResponse({'dishes': dishes_list})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            ingredients = data.get('ingredients')
            description = data.get('description')

            if ingredients is not None:
                dish = Dish.objects.create(name=name, description=description)
                for item in ingredients:
                    if item.get('name') is not None and item.get('quantity') is not None:
                        DishIngredient.objects.create(dish=dish, ingredient=Ingredient.objects.get(name=item.get(
                            'name')), quantity=item.get('quantity'))
                    else:
                        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
                return JsonResponse({'message': 'dish added successfully!'}, status=201)
            else:
                return JsonResponse({'error': 'ingredients are required.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            ingredients = data.get('ingredients')
            if name:
                try:
                    dish = Dish.objects.get(name=name)
                    if ingredients:
                        for item in ingredients:
                            dish_ingredient = DishIngredient.objects.get(dish=dish, ingredient=Ingredient.objects.get(name=item.get(
                                'name')), quantity=item.get('quantity'))
                            dish_ingredient.delete()
                        return JsonResponse({'message': 'ingredients in dish deleted successfully!'}, status=200)
                    else:
                        dish.delete()
                        return JsonResponse({'message': 'dish deleted successfully!'}, status=200)
                except Dish.DoesNotExist:
                    return JsonResponse({'error': 'dish does not exist.'}, status=404)

            else:
                return JsonResponse({'error': 'Name is required.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)


def report_ingredient(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ingredient_catalog.csv"'

    writer = csv.writer(response)
    writer.writerow(['Ingredient'])

    ingredients = Ingredient.objects.all()
    for ingredient in ingredients:
        writer.writerow([ingredient.name])

    return response


def report_dish(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Dish_catalog.csv"'

    writer = csv.writer(response)
    writer.writerow(['Dish name', 'Description', 'Ingredients', 'Quantity'])

    dishes = Dish.objects.all()
    for dish in dishes:
        ingredients = DishIngredient.objects.filter(dish=dish)
        ingredient_list = []
        quantity_list = []

        for ingredient in ingredients:
            ingredient_list.append(ingredient.ingredient.name)
            quantity_list.append(ingredient.quantity)

        writer.writerow([dish.name, dish.description,
                        ingredient_list,  quantity_list])

    return response
