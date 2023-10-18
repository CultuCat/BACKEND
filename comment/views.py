from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
#from usuaris import permissions
from .models import Comment
from .serializers import CommentSerializer


class CommentsView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    #permission_classes = [permissions.IsPerfil]

    # filter_backends = [DjangoFilterBackend, ]
    # filterset_fields = {
    #     'esdeveniment__codi': ['exact', 'in'],
    #     'creador__user__id': ['exact', 'in']
    # }

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['creador_id'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)