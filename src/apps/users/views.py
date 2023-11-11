from django.shortcuts import render


def auth(request):
    return render(request, "social_auth/login.html")
