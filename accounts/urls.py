from django.urls import path

from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('register/verify/', views.UserVerifyAccountView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
]
