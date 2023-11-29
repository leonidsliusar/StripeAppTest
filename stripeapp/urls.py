from django.urls import path

from . import views

urlpatterns = [
    path("item/<int:id>", views.ItemView.as_view(), name="item"),
    path("buy/<int:id>", views.BuyHandler.as_view(), name="buy"),
]
