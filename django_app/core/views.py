from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Review
from django.core.paginator import Paginator
import ast
from datetime import datetime

def index(request):
    #SELECT * FROM RESTAURANTS ORDER BY 'review_count' DESC LIMIT 10
    restaurant_list = Restaurant.objects.all().order_by('-review_count')

    attributes = [ast.literal_eval(restaurant.attributes) for restaurant in restaurant_list]
    categories = [restaurant.categories.replace("Restaurants, ", "").split(", ") for restaurant in restaurant_list]

    paginator = Paginator(list(zip(restaurant_list, attributes, categories)), 12)

    #I'll send the current page as a GET parameter. When the user clicks the next page, this value will increment and the next page's content will be returned
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    #Gets the 12 recipes associated with the current page number
    page_obj = paginator.get_page(page_number)

    start = max(1, int(page_number) - 4)

    return render(request, 'core/index.html', {
        'page_obj': page_obj,
        'range': list(range(start, start+9))
    })

def detail(request, id):
    restaurant = get_object_or_404(Restaurant, pk = id)

    dt = datetime.now()

    return render(request, 'core/detail.html', {
        'restaurant': restaurant,
        'categories': restaurant.categories.split(", "),
        'attributes': ast.literal_eval(restaurant.attributes),
        'hours': ast.literal_eval(restaurant.hours),
        'dow': dt.weekday(),
        'time': datetime.now().time()
    })