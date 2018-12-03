# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models


class CountryAdmin(admin.ModelAdmin):
        list_display = ('code', 'name')
        search_fields = ('name',)


class CommentAdmin(admin.ModelAdmin):
        list_display = ('text', 'created_by', 'post')


class UserProfileAdmin(admin.ModelAdmin):
        list_display =('user', 'birthday')
        search_fields=('user__username',)


admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Post)
admin.site.register(models.UserProfile, UserProfileAdmin)
