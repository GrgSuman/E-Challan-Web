from .import views
from django.urls import path
from django.contrib.auth.decorators import login_required


urlpatterns = [
   path("",views.welcome,name="welcome"),
   path("auth/login",views.Login.as_view(),name="login"),
   path("user",login_required(views.Home.as_view()),name="home"),
   path("dashboard",login_required(views.Dashboard.as_view()),name="dashboard"),
   path("auth/signup",views.UserSignUp.as_view(),name="signup"),
   path("logout",views.LogOut,name="logout"),
   path("not-active",views.UnactiveUser,name="not-active"),
   path("bill-details/<pk>",login_required(views.BillDetails.as_view()),name="bill-details"),
   path("update/<pk>",login_required(views.UpdateBill.as_view()),name="update"),
   path("update-profile/<pk>",login_required(views.UpdateUser.as_view()),name="update_user"),
   path("update-profile-photo",login_required(views.UpdateUserPhoto.as_view()),name="update-user-photo"),
   path("delete/<pk>",login_required(views.DeleteBill.as_view()),name="delete"),
   path("delete-user/<pk>",login_required(views.DeleteUser.as_view()),name="deleteUser"),
   path("change-user-status/<pk>",views.ChangeUserStatus.as_view())
]
