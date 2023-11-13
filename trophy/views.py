from rest_framework import viewsets, status
from .models import Trophy
from .serializers import TrophySerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from user.permissions import IsAdmin

class TrophyView(viewsets.ModelViewSet):
    queryset = Trophy.objects.all()
    serializer_class = TrophySerializer
    models = Trophy
    apply_permissions = False

    def get_permissions(self):
        if self.action == 'create' and self.apply_permissions:
            return [IsAdmin()]
        else:
            return []

    def create(self, request, *args, **kwargs):
        trophy = request.data.copy()
        serializer = self.get_serializer(data=trophy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
