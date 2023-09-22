from django.urls import path

from jwt_authenticate import views


app_name = 'jwt'

urlpatterns = [
    path('login/', views.JwtLoginView.as_view()),
    path('refresh/', views.JwtRefreshView.as_view()),
    path('verify/', views.JwtVerifyView.as_view()),
]
