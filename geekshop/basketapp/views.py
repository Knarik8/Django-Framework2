from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from basketapp.models import Basket
from django.template.loader import render_to_string
from django.urls import reverse

from mainapp.models import Product

@login_required

def basket(request):
    if request.user.is_authenticated:
        # basket = Basket.objects.filter(user=request.user)
        basket = request.user.basket.select_related()
        context = {
            'basket_items': basket,
        }
        return render(request, 'basket.html', context)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)
    old_basket_item = Basket.objects.filter(user=request.user, product=product)

    # old_basket_item = Basket.get_product(user=request.user, product=product)

    if old_basket_item:
        old_basket_item[0].quantity +=1
        old_basket_item[0].save()
    else:
        new_basket_item = Basket(user=request.user, product=product)
        new_basket_item.quantity +=1
        new_basket_item.save()


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
