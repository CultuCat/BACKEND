from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Discount
from .serializers import DiscountSerializer

class DiscountsView(viewsets.ModelViewSet):
    queryset = Discount.objects.filter(usat=False)
    serializer_class = DiscountSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userDiscount']

    def create(self, request, *args, **kwargs):
        discount = request.data.copy()
        discount['userDiscount'] = 1 #request.user #1
        serializer = self.get_serializer(data=discount)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        
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


# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from .models import Discount
# from rest_framework.decorators import api_view
# from .serializers import DiscountSerializer
# from user.permissions import IsAuthenticated 
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.views import APIView


# class DescuentoView(APIView):
#     queryset = Discount.objects.none()  # Agrega un queryset falso
    
#     def get(self, request):
#         codigo_descuento = request.query_params.get('discount')
#         usuario_actual = '1'#request.user
#         try:
#             descuento = Discount.objects.get(codi=codigo_descuento, userDiscount=usuario_actual, usat=False)
#             return Response({'existe_descuento': True}, status=status.HTTP_200_OK)
#         except Discount.DoesNotExist:
#             return Response({'existe_descuento': False}, status=status.HTTP_200_OK)


# class DescuentoView(APIView):
#     queryset = Discount.objects.none()  # Agrega un queryset falso
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['user']

#     def get(self, request):
#         queryset = Discount.objects.filter(usat=False)
#         serializer = DiscountSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)