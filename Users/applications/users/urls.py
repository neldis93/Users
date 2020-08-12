from django.urls import path

from .import views

app_name='users_app'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.LoginUserView.as_view(), name='user_login'),
    path('logout/', views.LogoutView.as_view(), name='user_logout'),
    path('update/', views.UpdatePasswordView.as_view(), name='update_password'),
    path('verification/<pk>/', views.CodeVerificationView.as_view(), name='user_verification'),
]