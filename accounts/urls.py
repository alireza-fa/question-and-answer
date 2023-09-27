from django.urls import path

from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('register/verify/', views.UserVerifyAccountView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    path('follow/<str:username>/', views.UserFollowView.as_view()),
    path('unfollow/<str:username>/', views.UserUnfollowView.as_view()),
    path('followers/', views.UserFollowerListView.as_view()),
    path('following/', views.UserFollowingListView.as_view()),
]
