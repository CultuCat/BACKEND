from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer
from user.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class CommentsView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    models = Comment
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    #permission_classes = True#[IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']
    
    apply_permissions = True

    def get_permissions(self):
        if self.action == 'create' and self.apply_permissions:
            return [IsAuthenticated]
        else:
            return []

    def create(self, request, *args, **kwargs):
        comment = request.data.copy()
        comment['user'] = 1 #request.user.id #1
        serializer = self.get_serializer(data=comment)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)