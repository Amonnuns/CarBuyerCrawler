
from django.contrib import admin
from django.urls import path
from CarSearcher import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index), 
    path('submit', views.search), 
    path('delete', views.delete) 
]
