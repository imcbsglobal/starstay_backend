from django.urls import path
from . import views

urlpatterns = [
    path("visitors/", views.visitor_list, name="visitor_list"),
    path("register/", views.user_register, name="visitor_register"),
    path("user-register/", views.user_register, name="user_register"),
    path("admin-login/", views.admin_login, name="admin_login"),

    # Showcase API
    path("showcase/", views.showcase_list, name="showcase_list"),
    path("showcase/<int:pk>/", views.showcase_detail, name="showcase_detail"),

    # Demonstrations API (ADD THESE)
    path("demonstrations/", views.demonstration_list, name="demonstration_list"),
    path("demonstrations/<int:pk>/", views.demonstration_detail, name="demonstration_detail"),

    # Dashboard
    path("dashboard/", views.dashboard_data, name="dashboard_data"),
]