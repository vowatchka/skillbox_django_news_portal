from django.urls import path
from .views import NewsPortalLogin, NewsPortalLogout

urlpatterns = [
    path("login/", NewsPortalLogin.as_view(), name="login"),
    path("logout/", NewsPortalLogout.as_view(), name="logout"),
]
