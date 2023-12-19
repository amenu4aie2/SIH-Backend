from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('doText/', views.doText, name='doText'),
    path('getEmp/', views.getEmp, name='getEmp')
    # Add more paths here
]
