from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # اگر کاربر لاگین نکرده و صفحه مورد نظر لاگین نباشه، به صفحه لاگین هدایت بشه
        if not request.user.is_authenticated and request.path != reverse('login'):
            return redirect('login')  # به صفحه لاگین هدایت میشه
        return self.get_response(request)