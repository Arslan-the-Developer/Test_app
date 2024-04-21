from django.urls import path,include
from tastepointapp import views

urlpatterns = [
    path('',views.index,name='index'),
]
