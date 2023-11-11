from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Discount
from rest_framework.decorators import api_view
from .serializers import DiscountSerializer
from user.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend

# class DiscountsView(viewsets.ModelViewSet):
#     queryset = Discount.objects.all()
#     serializer_class = DiscountSerializer
#     models = Discount

#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['userDiscount']

#     def create(self, request, *args, **kwargs):
#         discount = request.data.copy()
#         discount['user'] = 1 #request.user #1
#         serializer = self.get_serializer(data=discount)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
def verificar_descuento(request):
    # Obtén el código de descuento de la consulta
    codigo_descuento = request.query_params.get('codigo')
    # Obtén el usuario actual
    usuario_actual = '1'#request.user

    def get_permissions(self):
        if self.action == 'create' and self.apply_permissions:
            return [IsAuthenticated]
        else:
            return []
        
    # Verifica si un descuento con el código y el usuario especificados existe
    try:
        descuento = Discount.objects.get(codigo=codigo_descuento, userDiscount=usuario_actual, usat=False)
        return Response({'existe_descuento': True}, status=status.HTTP_200_OK)
    except Discount.DoesNotExist:
        return Response({'existe_descuento': False}, status=status.HTTP_200_OK)
    
# DESDE EL POST DE ENTRADA, SI EL CAMPO DISCOUNT NO ESTÁ VACÍO, YA SERÁ CORRECTO PORQ SE HA COMPROBADO EN FRONT, ASÍ QUE SIMPLEMENTE MARCARLO COMO USADO CON:
#     descuento = Descuento.objects.get(codigo=codigo_descuento)
#         # Cambia el valor de bool a True
#         descuento.bool = True
#         descuento.save()

# Y PARA HACER EL POST LO QUE SE HARÍA ES:
#     codigo_descuento = "asasa"
# usuario_descuento = ...  # El usuario para el descuento
# descripcion = ...  # Descripción del descuento
# puntos = ...  # Puntos del descuento

# # Crea un nuevo descuento utilizando el método create
# descuento = Descuento.objects.create(
#     codigo=codigo_descuento,
#     userDiscount=usuario_descuento,
#     descripcion=descripcion,
#     puntos=puntos,
#     bool=False  # El descuento se crea como no utilizado
# )