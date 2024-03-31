from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from training.models import (Activity, UserActivity, UserActivityLog, do_training)
from training.serializers import UserActivityLogSerializer


def get_user_from_request(request):
    if request.user.is_authenticated:
        return request.user

    user = User.objects.all().first()
    if not user:
        user = User.objects.create(username='user1')
    return user


class UserActivityLogAPIView(APIView):

    def get(self, request):
        activity_logs = UserActivityLog.objects.all()
        serializer = UserActivityLogSerializer(activity_logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = get_user_from_request(request)

        activity_id = data.get('activity_id')

        if not activity_id:
            raise serializers.ValidationError({"error": "id of activity is required"})

        activity = Activity.objects.get(id=activity_id)

        user_activity, created = UserActivity.objects.get_or_create(
            user=request.user,
            activity=activity,
            defaults={
                "completed": False
            }
        )

        if created:
            activity_log = UserActivityLog.objects.create(user_activity=user_activity, started_at=timezone.now())

            serializer = UserActivityLogSerializer(activity_log)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        data = request.data
        activity_log_id = data.get('activity_log_id')
        if not activity_log_id:
            raise serializers.ValidationError({"error": "id of user activity log is required"})

        activity_log = UserActivityLog.objects.get(id=activity_log_id)
        if not activity_log:
            raise serializers.ValidationError({"error": f"No activity log matching {activity_log_id}"})

        activity_log.score = do_training()

        completed = data.get('completed')
        if completed:
            activity_log.ended_at = timezone.now()
            user_activity = activity_log.user_activity
            user_activity.completed = True
            user_activity.save()

        activity_log.save()

        return Response(UserActivityLogSerializer(activity_log).data, status=status.HTTP_200_OK)


def index(request):
    return render(request, 'index.html')