from django.shortcuts import render


def TOS_page(request):
    return render(request, 'tos.html')