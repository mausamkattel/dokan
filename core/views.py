from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order
from shops.models import Shop
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    try:
        shop = Shop.objects.get(owner=request.user)
        products = shop.products.all().order_by('-id')
        dokan_orders = Order.objects.filter(
            product__shop=shop).order_by('completed')
    except Exception:
        shop = None
        products = None
        dokan_orders = None
    context = {
        'orders': Order.objects.filter(user=request.user),
        'dokanOrders': dokan_orders,
        'shop': shop,
        'products': products
    }

    return render(request, "core/dashboard.html", context)
