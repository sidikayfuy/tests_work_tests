from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.site_register, name='register'),
    path('login', views.site_login, name='login'),
    path('logout', views.site_logout, name='logout'),
    path('lk', views.lk, name='lk'),
    path('result/<id>', views.result, name='result'),
    path('test/<id>', views.test, name='test'),
    path('start/<id>', views.start_test, name='start_test'),
    path('test/<test_id>/question/<question_id>', views.question, name='question'),
]
