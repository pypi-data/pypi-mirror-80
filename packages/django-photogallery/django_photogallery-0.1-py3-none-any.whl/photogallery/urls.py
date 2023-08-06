from django.urls import path

from . import views

app_name = 'photogallery'
urlpatterns = [
    path('', views.PhotoIndexView.as_view(), name='index'),
    path('<int:pk>/', views.PhotoDetailView.as_view(), name='detail')
]
