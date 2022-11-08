from django.urls import path
from .views import CartItemViews


urlpatterns = [
    path('callback/', CartItemViews.as_view()),
    path('cart-items/<int:id>', CartItemViews.as_view())
]
