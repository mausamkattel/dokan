from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('status/<int:pk>/', views.status, name="status"),
    path('create/<int:pk>/', views.OrderCreateView.as_view(), name="order_create"),
]
