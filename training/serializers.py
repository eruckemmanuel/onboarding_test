from django.contrib.auth.models import User
from rest_framework import serializers

from training.models import UserActivity, UserActivityLog, Activity


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    activity = ActivitySerializer(read_only=True)

    class Meta:
        model = UserActivity
        fields = [
            'user',
            'activity',
            'completed',
            'created_at',
            'updated_at',
            'id'
        ]


class UserActivityLogSerializer(serializers.ModelSerializer):

    user_activity = UserActivitySerializer(read_only=True)

    class Meta:
        model = UserActivityLog
        fields = [
            'user_activity',
            'score',
            'created_at',
            'started_at',
            'ended_at',
            'id'
        ]
