from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),
    path('shops/', views.AllShopsView.as_view(), name="all-shops"),
    path('shops/detail/<slug:name>/',
         views.ShopDetailView.as_view(), name="shop-detail"),
    path('shops/create/',
         views.ShopCreateView.as_view(), name="create-shop"),
    path('shops/hide/<int:pk>/', views.hide_shop, name="hide-shop"),
    path('shops/activate/<int:pk>/', views.activate_shop, name="activate-shop"),
    path('shops/edit/<int:pk>', views.ShopEditView.as_view(), name="edit-shop"),
    path('shop/created/', views.ShopCreatedView.as_view(), name="shop-created"),
]
