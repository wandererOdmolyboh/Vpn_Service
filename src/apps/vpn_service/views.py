from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import UserSite, VPNUsage
from .forms import UserForm, UserProfileForm, UserSiteForm


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_f = profile_form.save(commit=False)
            profile_f.user = user
            profile_f.save()
            login(request, user)
            return redirect('profile')
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'vpn_service/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'vpn_service/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def user_sites(request):
    sites = UserSite.objects.filter(user=request.user)
    if request.method == 'POST':
        form = UserSiteForm(request.POST)
        if form.is_valid():
            user_site = form.save(commit=False)
            user_site.user = request.user
            user_site.save()
            return redirect('user_sites')
    else:
        form = UserSiteForm()
    return render(request, 'vpn_service/user_sites.html', {'sites': sites, 'form': form})


@login_required
def statistics(request):
    stats = VPNUsage.objects.filter(user=request.user).order_by('-date')
    return render(request, 'vpn_service/statistics.html', {'stats': stats})


@login_required
def create_site(request):
    if request.method == 'POST':
        form = UserSiteForm(request.POST)
        if form.is_valid():
            user_site = form.save(commit=False)
            user_site.user = request.user
            user_site.save()
            return redirect('site_list')
    else:
        form = UserSiteForm()
    return render(request, 'vpn_service/create_site.html', {'form': form})


@login_required
def site_list(request):
    sites = UserSite.objects.filter(user=request.user)
    return render(request, 'vpn_service/site_list.html', {'sites': sites})
