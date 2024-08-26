import requests

from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import UserSite, VPNUsage, UserProfile
from .forms import UserForm, UserProfileForm, UserSiteForm


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            UserProfile.objects.create(user=user, **profile_form.cleaned_data)
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
            UserSite.objects.create(user=request.user, **form.cleaned_data)
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
            UserSite.objects.create(user=request.user, **form.cleaned_data)
            return redirect('site_list')
    else:
        form = UserSiteForm()
    return render(request, 'vpn_service/create_site.html', {'form': form})


@login_required
def site_list(request):
    sites = UserSite.objects.filter(user=request.user)
    return render(request, 'vpn_service/site_list.html', {'sites': sites})


@login_required
def proxy_view(request, site_name, path):
    try:
        user_site = UserSite.objects.get(user=request.user, name=site_name)
    except UserSite.DoesNotExist:
        return HttpResponseNotFound("Site not found")

    target_url = f"{user_site.original_url}/{path}"
    response = requests.get(target_url, params=request.GET)
    # maybe append headers in request

    vpn_usage, _ = VPNUsage.objects.get_or_create(user=request.user, site=user_site,
                                                        date__date=timezone.now().date())
    vpn_usage.page_views += 1
    vpn_usage.data_received += len(response.content)
    vpn_usage.data_sent += len(request.body or b'')
    vpn_usage.save()

    content = response.content.decode('utf-8')
    content = content.replace(user_site.original_url, f"/{site_name}")
    return HttpResponse(content, status=response.status_code,)
