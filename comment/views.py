from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from django.shortcuts import get_object_or_404

from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet():
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # When a comment is created, associate it with the authenticated user
        #serializer.save(user=self.request.user)
        serializer.save()


    def get_queryset(self):
        # Customize the queryset for retrieving comments, e.g., filter by event
        event_id = self.request.query_params.get('event_id')
        if event_id:
            return Comment.objects.filter(event=event_id)
        return Comment.objects.all()
