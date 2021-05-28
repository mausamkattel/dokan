from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('<int:pk>/<slug:slug>/', views.ProductDetailView.as_view(), name="detail"),
    path('create/<int:pk>/', views.ProductCreateView.as_view(),
         name="product-create"),
    path('edit/<int:pk>/', views.ProductEditView.as_view(), name="product-edit"),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(),
         name="product-delete"),
    path('category/<slug:category>/',
         views.CategoryView.as_view(), name="category"),
    path('search/', views.SearchView.as_view(), name="search"),
]
