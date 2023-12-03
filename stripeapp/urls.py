from . import views
from django.urls import path


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("item/<int:id>", views.ItemView.as_view(), name="item"),
    path("buy/<int:id>", views.BuyHandler.as_view(), name="buy"),
    path("order/<int:id>", views.OrderView.as_view(), name="order"),
    path("order/by_item/<int:id>", views.OrdersByItemView.as_view(), name="item_in_orders"),
]
