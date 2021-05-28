from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order
from products.models import Product
from django.http import HttpResponseRedirect
from django.contrib import messages
from core.mail import email
from django.contrib.auth.decorators import login_required


@login_required
def status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.product.shop.owner == request.user:
        order.completed = not order.completed
        order.save()
    return redirect(reverse("core:dashboard"))


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = "orders/order_form.html"
    model = Order
    fields = ["quantity", "full_name",
              "address", "phone_number", "email"]
    success_url = "products:detail"

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['email'] = self.request.user.email
        initial['phone_number'] = self.request.user.phone
        initial['address'] = self.request.user.address
        initial['full_name'] = self.request.user.first_name + \
            " " + self.request.user.last_name
        return initial

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        data = super().get_context_data(**kwargs)
        data["product"] = get_object_or_404(Product, pk=self.kwargs['pk'])
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.product = Product.objects.get(pk=self.kwargs['pk'])
        self.object.save()
        subject = f"New Order Recieved for {self.object.product.name}"
        message = f"""
        {self.object.full_name} placed an order of {self.object.quantity} quantity of {self.object.product.name} \n
        Order Details: \n
        Quantity - {self.object.quantity} 
        By - {self.object.full_name} 
        Address - {self.object.address} 
        Number - {self.object.phone_number} 
        Email - {self.object.email} 

        * Please Visit https://dokanharu.com/info/dashboard to manage orders and see its detail.
        """
        email(self.object.product.shop.owner.email, subject, message)
        messages.success(
            self.request, 'Your order was successfully added. The seller or dokan will contact you soon.')
        return redirect(reverse(self.success_url, kwargs={"pk": self.object.product.pk, "slug": self.object.product.slug}))
