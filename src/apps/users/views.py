from django.shortcuts import render


def soc_auth(request):
    return render(request, "social_auth/login.html")
