from django.urls import path

from . import views

urlpatterns = [
    path("item/<int:id>", views.ItemView.as_view(), name="item"),
    path("buy/<int:id>", views.BuyHandler.as_view(), name="buy"),
    path("order/<int:id>", views.OrderView.as_view(), name="order"),
    path("item/by_order/<int:id>", views.OrdersByItemView.as_view(), name="item_in_orders")
]
