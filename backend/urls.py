from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('doText/', views.doText, name='doText'),
    # Add more paths here
]
