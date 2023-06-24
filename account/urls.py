from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('singup/',views.UserSingupView.as_view(),name='user_singup'),
    path('login/',views.UserLoginView.as_view(), name='user_login'),
    path('profile/<int:user_id>',views.UserProfileView.as_view(), name='user_profile'),
    path('logout/',views.UserLogoutView.as_view(), name='user_logout'),
    path('update/<int:user_id>',views.UserUpdateProfileView.as_view(), name='user_profileupdate'),
    path('rest/',views.PasswordResetView.as_view(), name='reset_password'),
    path('reset/done/',views.PasswordResetDoneView.as_view(), name = 'password_rest_done'),
    path('confrim/<uidb64>/<token>/',views.PasswordResetConfrimView.as_view(), name='password_reset_confrim'),
    path('confrim/complete/',views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/<int:user_id>/transactions/', views.UserTransactions.as_view(), name='user_transactions'),
]