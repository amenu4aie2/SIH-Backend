from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('doText/', views.doText, name='doText'),
    path('getEmp/', views.getEmp, name='getEmp'),
    path('getEmps/', views.getEmps, name='getEmps'),
    path('replme/', views.replme, name='replme'),
    # Add more paths here
]
