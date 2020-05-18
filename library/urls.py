from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('search', views.search, name='search'),
    path('borrow', views.borrow, name='borrow'),
    path('function', views.function, name='function'),
    path('renew', views.renew, name='renew'),
    path('return_book', views.return_book, name='return_book'),
]