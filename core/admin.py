from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core import models


admin.site.register(models.Tasks)
admin.site.register(models.Users)
admin.site.register(models.FriendshipInvite)
