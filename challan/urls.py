from .import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
   path("",views.welcome,name="welcome"),

   path("auth/login",views.Login.as_view(),name="login"),

   path("home",login_required(views.Home.as_view()),name="home"),

   path("auth/signup",views.UserSignUp.as_view(),name="signup"),

   path("logout",views.LogOut,name="logout"),

   path("update/<pk>",login_required(views.UpdateBill.as_view()),name="update"),

   path("update-profile/<pk>",login_required(views.UpdateUser.as_view()),name="update_user"),

   path("update-profile-photo",login_required(views.UpdateUserPhoto.as_view()),name="update-user-photo"),

   path("delete/<pk>",login_required(views.DeleteBill.as_view()),name="delete"),

   path("delete-user/<pk>",login_required(views.DeleteUser.as_view()),name="deleteUser"),

   path("change-user-status/<pk>",views.ChangeUserStatus.as_view()),

   # path("print-bill/<pk>",views.GeneratePdf.as_view(),name="printBill"),
   path("print-bill/<pk>",views.downloadBill,name="printBill"),

   path('reset_password/', auth_views.PasswordResetView.as_view(),name="reset_password"),
   path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
   path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]
