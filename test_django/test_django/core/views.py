from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from django_messages.models import Message
from django.contrib.auth.models import User
from django_messages.forms import ComposeForm
from .serializers import MessageSerializer, MessageCreateSerializer


class MessageView(APIView):
    def get(self, request, pk):
        u = User.objects.filter(id=pk)
        message_list = Message.objects.inbox_for(u[0])
        serializer = MessageSerializer(message_list, many=True)
        return Response({
            "message_list": serializer.data,
            })

class MessageUnreadView(APIView):
    def get(self, request, pk):
        u = User.objects.filter(id=pk)
        unread_messages = Message.objects.filter(recipient=u[0], read_at__isnull=True)
        serializer_unread_messages = MessageSerializer(unread_messages, many=True)
        return Response({
            "unread_messages": serializer_unread_messages.data,
            })

class MessageLastView(APIView):
    def get(self, request, pk):
        message_list = Message.objects.filter(id=pk)
        sender = message_list.reverse()[0].sender.username
        subject = message_list.reverse()[0].subject
        body = message_list.reverse()[0].body
        sent_at = message_list.reverse()[0].sent_at
        return Response({
            'sender': sender,
            'subject': subject,
            "body": body,
            "sent_at": sent_at,
            })

class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer

    def create(self, request, *args, **kwargs):
        super(MessageCreateView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)


# {
#     "sender_id": "2",
#     "recipient_id": "3",
#     "subject": "api_test",
#     "body": "thjhjhjjjj"
# }

class MessageDelView(APIView):
    def delete(self, request, id_u, pk):
        u = User.objects.filter(id=id_u)
        try:
            message = get_object_or_404(Message.objects.inbox_for(u[0]), pk=pk)
        except:
            message = get_object_or_404(Message.objects.outbox_for(u[0]), pk=pk)
        message.delete()
        return Response({
            "message": "Message with id `{}` has been deleted.".format(pk)
        }, status=204)

