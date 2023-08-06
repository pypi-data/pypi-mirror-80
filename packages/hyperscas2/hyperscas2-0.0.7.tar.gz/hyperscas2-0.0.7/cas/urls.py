from django.urls import path, re_path

from . import views

app_name = "cas"

urlpatterns = [
    path("logout", views.logout, name="logout"),
    path("user/language", views.language, name="language"),
    path("environment", views.enviroment, name="environment"),
    re_path("^user/profile$|^user$", views.profile, name="profile"),
    path("user/settings", views.settings, name="settings"),
    path("file/upload", views.upload, name="upload"),
]
