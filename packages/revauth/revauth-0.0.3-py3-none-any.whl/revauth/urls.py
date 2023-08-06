from django.urls import path
from revauth import views

urlpatterns = [
    path('google', views.GoogleLogin.as_view(), name='auth-google'),
    path('facebook', views.FacebookLogin.as_view(), name='auth-facebook'),
    path('validation/request', views.ValidationView.as_view(), name='auth-validation'),
    path('user/register', views.UserRegister.as_view(), name='auth-register'),
]
