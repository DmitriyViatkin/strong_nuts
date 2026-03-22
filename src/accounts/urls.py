from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-recovery/',views.PasswordRecoveryView.as_view(),     name='password-recovery'),
    path('password-reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(), name='password-reset'),
    path("change-password/", views.CustomPasswordChangeView.as_view(), name="change_password"),

]