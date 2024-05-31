from django.urls import path
from . import views


urlpatterns = [
    path("login",views.login_page, name="login"),
    path("register",views.register_page, name="register"),
    path('profile/<str:username>/', views.profile_view, name="profile"),
    path("settings",views.setting_page, name="settings"),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('delete-profile-picture/', views.delete_profile_picture, name='delete_profile_picture'),
    path('logging-out',views.logging_out, name='logging_out')
]
