from django.urls import path

from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('register/verify/', views.UserVerifyAccountView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    path('profile/update/', views.UserProfileEditView.as_view()),
    path('contacts/add/', views.ContactCreateView.as_view()),
    path('contacts/delete/<int:contact_id>/', views.UserContactDelete.as_view()),
    path('profile/other/<str:username>/', views.UserProfileOtherView.as_view()),
    path('follow/<str:username>/', views.UserFollowView.as_view()),
    path('unfollow/<str:username>/', views.UserUnfollowView.as_view()),
    path('followers/<str:username>/', views.UserFollowerListView.as_view()),
    path('followings/<str:username>/', views.UserFollowingListView.as_view()),
]
