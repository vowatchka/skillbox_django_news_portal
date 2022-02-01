from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings


class NewsPortalLogin(LoginView):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        next_page = request.headers.get("referer", settings.LOGIN_REDIRECT_URL)
        if "/register/" in next_page:
            next_page = "/"

        response.context_data["next_page"] = next_page
        return response


class NewsPortalLogout(LogoutView):
    pass
