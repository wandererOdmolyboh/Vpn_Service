from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


class UserSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    original_url = models.URLField()

    def __str__(self):
        return self.name


class VPNUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(UserSite, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    page_views = models.PositiveIntegerField(default=0)
    data_sent = models.PositiveIntegerField(default=0)  # В байтах
    data_received = models.PositiveIntegerField(default=0)  # В байтах

    def __str__(self):
        return f"Usage for {self.site.name} by {self.user.username}"
