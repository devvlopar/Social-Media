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
    path('email_otp/', views.email_otp, name='email_otp'),
    path('add_post/', views.add_post, name='add_post'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_email/', views.change_email, name='change_email'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('comment/<int:pk>', views.comment, name='comment'),
    path('comment_session/<int:pk>', views.comment_session, name='comment_session'),
    path('like/<int:pk>', views.like, name="like"),
    path('like_session/<int:pk>', views.like_session, name="like_session"),
    path('unlike_session/<int:pk>', views.unlike_session, name="unlike_session"),
    path('unlike/<int:pk>', views.unlike, name="unlike"),
    path('follow/<int:pk>', views.follow, name="follow"),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('other_user_profile/<int:pk>', views.other_user_profile, name='other_user_profile'),
    path('view_followers/<int:pk>', views.view_followers, name='view_followers'),
    path('view_following/<int:pk>', views.view_following, name='view_following'),
    path('search/', views.search, name='search'),
    path('view_posts/', views.view_posts, name='view_posts'),
    path('notification/', views.notification, name='notification'),



]