from django.urls import path
from . import views
from .views import SneakerList

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sneakers/', views.sneakers_index, name='index'),
    path('sneakers/sneaker_list/', views.SneakerList.as_view(), name='sneaker_list'),
    path('sneakers/<int:sneaker_id>/', views.sneakers_detail, name='detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('sneakers/create/', views.SneakerCreate.as_view(), name='sneakers_create'),
    path('sneakers/<int:pk>/update/', views.SneakerUpdate.as_view(), name='sneakers_update'),
    path('sneakers/<int:pk>/delete/', views.SneakerDelete.as_view(), name='sneakers_delete'),
    path('sneakers/<int:sneaker_id>/add_photo/', views.add_photo, name='add_photo'),
]



