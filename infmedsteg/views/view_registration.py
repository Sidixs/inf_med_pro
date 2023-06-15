from django.contrib.auth import login
from django.shortcuts import redirect, render
from infmedsteg.forms import RegisterForm


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {"form": form})


