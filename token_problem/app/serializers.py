from rest_framework import serializers
from app.models import Token
from utils.utility import datetime_to_epoch


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
            "id",
            "token",
            "created_time",
            "expire_time",
            "last_used",
            "is_assigned",
        )

    def to_representation(self, instance):

        _temp = {
            "id": instance.id,
            "token": instance.token,
            "created_time": datetime_to_epoch(date_time=instance.created_time),
            "expire_time": datetime_to_epoch(date_time=instance.expire_time),
            "last_used": datetime_to_epoch(date_time=instance.last_used),
            "is_assigned": instance.is_assigned,
        }
        return _temp
