from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import Group, Permission

from .forms import RegisterForm
from .models import Profile

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            get_user = Profile.objects.get(id=user.id)
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
