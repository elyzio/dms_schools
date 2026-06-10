from django.urls import path
from .views import (
    UserListView, UserGroupUpdateView,
    UserProfileView, UserProfileUpdateView, UserProfilePasswordView,
)

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/grupo/', UserGroupUpdateView.as_view(), name='user-group'),

    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('profile/password/', UserProfilePasswordView.as_view(), name='user-profile-password'),
]
