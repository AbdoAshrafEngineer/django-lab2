from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse("login"),
            reverse("admin:login"),
            reverse("register")
        ]
        if hasattr(settings, "LOGIN_EXEMPT_URLS"):
            self.exempt_urls += settings.LOGIN_EXEMPT_URLS

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(path.startswith(url) for url in self.exempt_urls):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)
