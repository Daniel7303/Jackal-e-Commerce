from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.



def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('core:home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form':form})



def login_user(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(next_url or 'core:home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'next': next_url  # <-- pass next to template!
    })




def logout_user(request):
    if request.method == "POST":
        logout(request)
    return redirect("core:home")