from django.shortcuts import render
from .models import Restaurant, Review
import ast

def index(request):
    #SELECT * FROM RESTAURANTS ORDER BY 'review_count' DESC LIMIT 10
    restaurant_list = Restaurant.objects.all().order_by('-review_count')[:10]

    attributes = [ast.literal_eval(restaurant.attributes) for restaurant in restaurant_list]
    categories = [restaurant.categories.replace("Restaurants, ", "").split(", ") for restaurant in restaurant_list]

    return render(request, 'core/index.html', {
        'restaurants': zip(restaurant_list, attributes, categories),
    })