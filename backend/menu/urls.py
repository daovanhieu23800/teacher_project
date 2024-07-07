from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ingredient', views.ingredient, name='ingredient'),
    path('dish', views.dish, name='dish'),
    path('report/ingredient', views.report_ingredient,
         name='generate_ingredient_csv'),
    path('report/dish', views.report_dish,
         name='generate_dish_csv'),
]
