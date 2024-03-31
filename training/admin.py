from django.contrib import admin

from training.models import (Activity, UserActivity, UserActivityLog)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'is_active')


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('activity', 'user', 'created_at', 'updated_at', 'completed')


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user_activity', 'created_at', 'started_at', 'ended_at', 'score')
