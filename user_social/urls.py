from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('otp/', views.otp_fun, name='otp'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot/', views.forgot, name='forgot'),
    path('profile/', views.profile, name='profile'),
    path('forgot/', views.forgot, name='forgot'),


    

    path('notification/', views.notification, name='notification'),






]