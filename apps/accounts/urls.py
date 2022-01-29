from django.urls import path

from apps.accounts import views as accounts_views


urlpatterns = [
    path('register', accounts_views.RegisterUserView.as_view(), name='register'),
    path('login', accounts_views.LoginUserView.as_view(), name='login'),
    path('logout', accounts_views.LogoutUserView.as_view(), name='logout'),
    path('profile', accounts_views.UserProfileView.as_view(), name='profile'),
    path('update', accounts_views.UpdateUserView.as_view(), name='update'),
]
