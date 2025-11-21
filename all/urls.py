from django.urls import path
from all import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("login_success/", views.login_success, name="login_success"),
    path("admin_add/", views.add_user, name="add_user"),
    path("admin_edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path("admin_delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("admin_logout/", views.admin_logout, name="admin_logout"),

]
