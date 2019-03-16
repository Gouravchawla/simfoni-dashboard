from django.urls import path

from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.data, name='data'),
    path('create-chart/', views.create_chart, name='create_chart'),
]
