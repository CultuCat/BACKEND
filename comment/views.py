from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Comment
from discount.models import Discount
from .serializers import CommentSerializer
from user.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from utility.new_discount_utils import verificar_y_otorgar_descuento

class CommentsView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    models = Comment
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    #permission_classes = True#[IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']
    
    apply_permissions = False

    def get_permissions(self):
        if self.action == 'create' and self.apply_permissions:
            return [IsAuthenticated]
        else:
            return []

    def create(self, request, *args, **kwargs):
        comment = request.data.copy()
        comment['user'] = 1 #request.user #1
        serializer = self.get_serializer(data=comment)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        verificar_y_otorgar_descuento(comment['user'], "Reviwer", Comment.objects.filter(user= comment['user']).count())  
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# def verificar_y_otorgar_descuento(user_id):
#     t_comments = Trophy.objects.get(nom="Reviwer")
#     num_comments = Comment.objects.filter(user='1').count()
        
#     if num_comments == t_comments.punts_nivell1:
#         nivell = 1
#     elif num_comments == t_comments.punts_nivell2:
#         nivell = 2
#     elif num_comments == t_comments.punts_nivell3:
#         nivell = 3
        
#     caracteres_validos_codigo = string.ascii_uppercase + string.digits
#     codigo_descuento= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
#     while(Discount.objects.get(codi="codigo_descuento") == any):
#         codigo_descuento = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
            
#     Discount.objects.create(codi=codigo_descuento,userDiscount='1',nivellTrofeu=nivell,nomTrofeu='Reviwer',bool=False)