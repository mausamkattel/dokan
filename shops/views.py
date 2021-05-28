from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from products.models import Product
from users.models import User
from shops.models import Shop, Banner, Category
from django.contrib import messages


def hide_shop(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if shop.owner.id == request.user.id:
        shop.hide = True
        shop.save()
        messages.success(
            request, f'Your Dokan was successfully hid. You can activate it later!')
    return redirect(reverse('core:dashboard'))


def activate_shop(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if shop.owner.id == request.user.id:
        shop.hide = False
        shop.save()
        messages.success(
            request, f'Your Dokan is activated again!')
    return redirect(reverse('core:dashboard'))


class ShopCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Shop
    fields = ["name", "address", "category",
              "pan_number", "description", "image"]
    success_url = "shops:shop-created"
    template_name = "shops/shop_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = User.objects.get(pk=self.request.user.pk)
        self.object.owner = user
        user.is_seller = True
        user.save()
        self.object.save()
        messages.success(
            self.request, f'Your new Dokan was successfully added to Dokanharu.')
        return redirect(reverse(self.success_url))


class ShopEditView(LoginRequiredMixin, generic.UpdateView):
    model = models.Shop
    fields = ["name", "address", "category",
              "pan_number", "description", "image"]
    success_url = "core:dashboard"
    template_name = "shops/shop_edit.html"

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, f'Your Dokan is successfully edited')
        return redirect(reverse(self.success_url))


class HomePageView(View):
    def get(self, request):

        featured_products = Product.objects.filter(
            featured=True).filter(block=False)
        featured_shops = Shop.objects.filter(
            featured=True).filter(block=False)
        newest_products = Product.objects.filter(block=False)[:30]
        banners = Banner.objects.all().filter(block=False)
        context = {
            "featured_products": featured_products,
            "newest_products": newest_products,
            "banners": banners,
            "featured_shops": featured_shops,

        }
        return render(request, 'shops/index.html', context)


class ShopCreatedView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'shops/shop_created.html')


class AllShopsView(generic.ListView):
    template_name = "shops/shop_list.html"
    context_object_name = "shops"
    paginate_by = 60

    def get_queryset(self):
        category = self.request.GET.get('category', 'all')
        shops = Shop.objects.all().filter(
            hide=False).filter(block=False).order_by('-id')
        if category != "all":
            try:
                item = get_object_or_404(Category, slug=category)
                shops = shops.filter(category=item)

            except Exception:
                pass
        return shops

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context["categories_list"] = categories
        context['category'] = self.request.GET.get('category', 'all')
        return context


class ShopDetailView(generic.ListView):
    model = Shop
    template_name = "shops/shop_detail.html"
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        shop = get_object_or_404(Shop, slug=self.kwargs['name'])
        products = shop.products.all()
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop"] = get_object_or_404(Shop, slug=self.kwargs['name'])
        return context
