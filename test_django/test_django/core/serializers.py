from rest_framework import serializers
from django_messages.models import Message
from django.utils import timezone



class MessageSerializer(serializers.Serializer):
    sender = serializers.CharField()
    subject = serializers.CharField(max_length=140)
    sent_at = serializers.DateTimeField(default=timezone.now())
    body = serializers.CharField()


class MessageCreateSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField()
    recipient_id = serializers.IntegerField()
    subject = serializers.CharField(max_length=140)
    body = serializers.CharField()

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
