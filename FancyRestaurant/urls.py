"""FancyRestaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from App import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('create', views.create_guest, name='create'),
    path('reserve_list', views.list_reservation, name='reserve_list'),
    path('do_login', views.do_login),
    path('do_logout', views.do_logout),
    path('do_create', views.do_create),
    path('do_reserve', views.do_reserve),
]
