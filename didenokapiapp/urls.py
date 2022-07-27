from django.urls import path
from . import views


urlpatterns = [
    path('nodes/', views.ShopUnitView.as_view()),
    path('import/', views.ShopUnitCreateView.as_view()),
]