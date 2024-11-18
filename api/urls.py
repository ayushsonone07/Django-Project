from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("", views.HomeView.as_view(), name="HomeView"),
    path("users/register/", views.RegisterView.as_view(), name='RegisterView'),
    path("users/login/", views.LoginView.as_view(), name='LoginView'),
    path("users/logout/", views.LogoutView.as_view(), name='LogoutView'),
    path("staff/login/", views.StaffRegisterView.as_view(), name="StaffView"),
    path("users/get_user/", views.getUserView.as_view(), name='getUserView'),
    path("users/leaves/", views.LeaveView.as_view(), name='LeaveView'),
    path("token/refresh/", TokenRefreshView.as_view(), name='refresh'),
    path("token/verify_token/", TokenVerifyView.as_view(), name='verify_token'),
    path('leave/', views.SuperUserLeaveView.as_view(), name="SuperView")
    
]