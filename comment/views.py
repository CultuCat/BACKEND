from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comment
from .serializers import CommentSerializer

@api_view(['POST'])
def post_comment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_comments_for_event(request, event_id):
    comments = Comment.objects.filter(event=event_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# class CommentsView(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     #permission_classes = [permissions.IsPerfil]

#     # filter_backends = [DjangoFilterBackend, ]
#     # filterset_fields = {
#     #     'esdeveniment__codi': ['exact', 'in'],
#     #     'creador_user_id': ['exact', 'in']
#     # }

#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         data['creador_id'] = request.user.id
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)