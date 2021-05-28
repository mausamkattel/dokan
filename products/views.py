from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, DeleteView, ListView
from . import models
from shops.models import Shop, Category
from django.db.models import Q
from django.contrib import messages


class ProductDeleteView(DeleteView):
    model = models.Product
    success_url = "core:dashboard"
    template_name = "products/product_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(
            self.request, 'Your product was successfully deleted')
        return redirect(reverse(self.success_url))


class ProductCreateView(CreateView):
    model = models.Product
    fields = ["name", "sub_title", "description", "price", "discounted_price", "main_image", "image1",
              "image2", "image3", "image4", "in_stock", "sku", "brand", "category", ]
    template_name = "products/product_create.html"

    def render_to_response(self, context, **response_kwargs):
        shop = get_object_or_404(Shop, pk=self.kwargs.get('pk'))
        if shop.limited:
            if shop.products.count() >= 20:
                return redirect(reverse("core:dashboard"))
        return super().render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        shop = get_object_or_404(Shop, pk=self.kwargs.get('pk'))
        self.object.shop = shop
        self.object.save()
        messages.success(
            self.request, f'{self.object.name} was successfully added to Trade Nepal.')
        return redirect(self.get_success_url())


class ProductEditView(UpdateView):
    model = models.Product
    fields = ["name", "description", "price", "discounted_price", "main_image", "image1",
              "image2", "image3", "image4", "in_stock", "sku", "brand", "category", ]
    template_name = "products/product_edit.html"

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, f'Your product was successfully edited.')
        return redirect(self.get_success_url())


class ProductDetailView(DetailView):
    model = models.Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context["product"]
        shop_products = models.Product.objects.filter(
            shop=product.shop).filter(block=False)
        context["shop_products"] = shop_products
        return context


class SearchView(ListView):
    template_name = "products/search.html"
    paginate_by = 20
    context_object_name = "products"

    def get_queryset(self):
        sort = self.request.GET.get('sort', '')
        category = self.request.GET.get('category', 'all')
        products = models.Product.objects.filter(
            Q(shop__name__icontains=self.request.GET.get('term', '')) |
            Q(name__icontains=self.request.GET.get('term', '')) |
            Q(sub_title__icontains=self.request.GET.get('term', '')) |
            Q(description__icontains=self.request.GET.get('term', ''))
        ).filter(block=False)
        if category != "all":
            try:
                item = get_object_or_404(Category, slug=category)
                products = products.filter(category=item)
            except Exception:
                pass

        if sort == "latest":
            products = products.order_by('-date_added')
        elif sort == "price high to low":
            products = products.order_by('-price')
        elif sort == "price low to high":
            products = products.order_by('price')
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context["categories_list"] = categories
        return context


class CategoryView(ListView):
    template_name = "products/category.html"
    paginate_by = 20
    context_object_name = "products"

    def get_queryset(self):
        sort = self.request.GET.get('sort', '')
        item = get_object_or_404(Category, slug=self.kwargs['category'])
        products = models.Product.objects.filter(
            category=item).filter(block=False)

        if sort == "latest":
            products = products.order_by('-date_added')
        elif sort == "price high to low":
            products = products.order_by('-price')
        elif sort == "price low to high":
            products = products.order_by('price')
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context["categories_list"] = categories
        context["category"] = self.kwargs['category']

        return context
