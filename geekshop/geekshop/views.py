from django.shortcuts import render
from mainapp.models import Product, ProductCategory

from basketapp.models import Basket


def main(request):

    # products = Product.objects.all()[:3]
    products = Product.objects.filter().select_related('category')[:3]


    basket=''
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    context = {
        'slogan': 'Мега-удобные стулья',
        'topic': 'Тренды',
        'products': products,
        'basket': basket,

    }
    return render(request, 'index.html', context=context)

def contact(request):
    return render(request, 'contact.html')