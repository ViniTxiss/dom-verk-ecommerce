from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('products:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bem-vindo(a) à DOM VERK, {user.first_name}!')
            return redirect('products:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


from axes.exceptions import AxesBackendPermissionDenied, PermissionDenied


def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:home')
    if request.method == 'POST':
        try:
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                next_url = request.GET.get('next')
                # M2: Validar next_url para evitar Open Redirect
                if next_url and url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    pass  # next_url é seguro, usar como está
                else:
                    next_url = 'dashboard:home' if user.is_staff else 'products:home'
                messages.success(request, f'Olá, {user.first_name or user.username}!')
                return redirect(next_url)
        except (AxesBackendPermissionDenied, PermissionDenied):
            return render(request, 'accounts/lockout.html', status=403)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('products:home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
