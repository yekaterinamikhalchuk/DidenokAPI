from django.urls import path
from . import views


urlpatterns = [
    path('nodes/<int:pk>/', views.ShopUnitView.as_view()),
    path('import/', views.ShopUnitCreateView.as_view()),
    path('delete/<pk>/', views.EventDetail.as_view(), name='delete_event')
]