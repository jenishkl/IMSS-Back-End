from rest_framework import serializers
from newapp.model_s.CommonModels import Notifications


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = "__all__"
