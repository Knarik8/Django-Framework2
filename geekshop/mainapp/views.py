import random

from basketapp.models import Basket
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from mainapp.models import ProductCategory, Product


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.all()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.all()


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]

def get_same_products(hot_products):
    same_products = Product.objects.filter(category=hot_products.category).exclude(pk=hot_products.pk)[:3]

    return same_products
#
# def products(request, pk=None, page=1):
#     title = 'продукты'
#     category = ''
#     products = ''
#     # links_menu = ProductCategory.objects.all()
#
#     categories = ProductCategory.objects.all()
#     # basket = get_basket(request.user)
#
#     if pk:
#         if pk == 0:
#             category = {
#                 'pk': 0,
#                 'name': 'Все'
#             }
#         else:
#             category = get_object_or_404(ProductCategory, pk=pk)
#             # products = Product.objects.filter(category_id__pk=pk).order_by('price')
#             products = Product.objects.filter(category_id__pk=pk).select_related().order_by('price')
#
#
#         paginator=Paginator(products, 2)
#         try:
#             products_paginator=paginator.page(page)
#         except PageNotAnInteger:
#             products_paginator=paginator.page(1)
#         except EmptyPage:
#             products_paginator=paginator.page(paginator.num_pages)
#
#
#     hot_product = get_hot_product()
#     same_products = get_same_products(hot_product)
#
#     context = {
#         'title': title,
#         'categories': categories,
#         'category': category,
#         'links_menu': get_links_menu(),
#         'products': products_paginator,
#         # 'basket': basket,
#         'hot_product': hot_product,
#         'same_products': same_products,
#     }
#     return render(request, 'products_list.html', context=context)


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)
    basket = get_basket(request.user)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    if pk:
        if pk == '0':
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'hot_product': hot_product,
            'category': category,
            'products': products_paginator,
            'basket': basket,
        }

        return render(request, 'products_list.html', content)

    content = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': basket,
    }

    return render(request, 'products.html', content)


@login_required
def product(request, pk):
    title = 'страница продукта'
    # product: get_object_or_404(Product, pk=pk)

    product = get_product(pk)

    context = {
        'title': title,
        'product': product,
        'links_menu': get_links_menu(),
        # 'basket': get_basket(request.user),
        # 'categories': ProductCategory.objects.all(),
        'categories': ProductCategory.objects.filter().select_related()

    }

    return render(request, 'product.html', context)
