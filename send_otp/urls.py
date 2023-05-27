from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

app_name = 'OTP'
urlpatterns = [
    path('login/', views.LoginOtpView.as_view(), name='login'),
    path('verify/', views.VerifyOtp.as_view(), name='verify'),
    path('home/', views.UserAuth.as_view(), name='home'),
    
    path('post/', views.UserGetView.as_view(), name='post'),
    path('post/create/', views.UserCreateView.as_view(), name='create'),
    path('post/update/<slug:slug>/', views.UserUpdateView.as_view(), name='update'),
    path('post/delete/<slug:slug>/', views.UserdeleteView.as_view(), name='delete'),

    path('refresh/', TokenRefreshView.as_view())
]   
 