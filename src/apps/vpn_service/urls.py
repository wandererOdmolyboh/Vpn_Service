from django.urls import path, re_path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('statistics/', views.statistics, name='statistics'),
    path('sites/', views.site_list, name='site_list'),
    path('sites/create/', views.create_site, name='create_site'),
    re_path(r'^(?P<site_name>[^/]+)/(?P<path>.*)$', views.proxy_view, name='proxy_view'),
]
