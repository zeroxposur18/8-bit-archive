from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name ='search'),
    path('about/', views.about, name='about'),
    path('collections/', views.collections_index, name='index'),
    path('accounts/signup', views.signup, name='signup'),
]
