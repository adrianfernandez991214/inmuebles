from inmuebleslist_app.models import Inmueble, Tienda, Comentario
from inmuebleslist_app.api.serializers import InmuebleSerializers, TiendaSerializers, ComentarioSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from inmuebleslist_app.api.permissions import IsAdminOrReadOnly, IsComentarioUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from inmuebleslist_app.api.throttling import InmuebleDetalleThrottle, InmuebleListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from inmuebleslist_app.api.pagination import InmuebleLOPagination

# metodo detallo para logica compleja


class UsuarioComentario(generics.ListAPIView):
    serializer_class = ComentarioSerializers

    # def get_queryset(self):
    #    username = self.kwargs['username']
    #    return Comentario.objects.filter(comentario_user__username=username)

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Comentario.objects.filter(comentario_user__username=username)


class Tienda_listAV(APIView):

    def get(self, request):
        tiendas = Tienda.objects.all()
        serializer = TiendaSerializers(
            tiendas, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        de_serilizer = TiendaSerializers(data=request.data)
        if de_serilizer.is_valid():
            de_serilizer.save()
            return Response(de_serilizer.data)
        else:
            return Response(de_serilizer.errors)


# metodo detallo para logica compleja
class Tienda_detalleAV(APIView):

    def get(self, request, pk):
        try:
            tienda = Tienda.objects.get(pk=pk)
            serializer = TiendaSerializers(
                tienda, context={'request': request})
            return Response(serializer.data)
        except Tienda.DoesNotExist:
            return Response({'Error': 'La tienda no existe'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            tienda = Tienda.objects.get(pk=pk)
            de_serilizer = TiendaSerializers(tienda, data=request.data)
            if de_serilizer.is_valid():
                de_serilizer.save()
                return Response(de_serilizer.data)
            else:
                return Response(de_serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Tienda.DoesNotExist:
            return Response({'Error': 'La tienda no existe'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            tienda = Tienda.objects.get(pk=pk)
            tienda.delete()
        except Tienda.DoesNotExist:
            return Response({'Error': 'La tienda no existe'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

# Para casos genricos


class TiendaVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializers


class Inmueble_lista_filter(generics.ListAPIView):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializers
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['direccion', 'tienda__nombre']
    pagination_class = InmuebleLOPagination


class Inmueble_listAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [InmuebleListThrottle]

    def get(self, request):
        inmuebles = Inmueble.objects.all()
        serializer = InmuebleSerializers(inmuebles, many=True)
        return Response(serializer.data)

    def post(self, request):
        de_serilizer = InmuebleSerializers(data=request.data)
        if de_serilizer.is_valid():
            de_serilizer.save()
            return Response(de_serilizer.data)
        else:
            return Response(de_serilizer.errors)


class Inmueble_detalleAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            inmueble = Inmueble.objects.get(pk=pk)
            serializer = InmuebleSerializers(inmueble)
            return Response(serializer.data)
        except Inmueble.DoesNotExist:
            return Response({'Error': 'Inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            inmueble = Inmueble.objects.get(pk=pk)
            de_serilizer = InmuebleSerializers(inmueble, data=request.data)
            if de_serilizer.is_valid():
                de_serilizer.save()
                return Response(de_serilizer.data)
            else:
                return Response(de_serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Inmueble.DoesNotExist:
            return Response({'Error': 'Inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            inmueble = Inmueble.objects.get(pk=pk)
            inmueble.delete()
        except Inmueble.DoesNotExist:
            return Response({'Error': 'Inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class Cometario_Create(generics.CreateAPIView):
    serializer_class = ComentarioSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comentario.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        inmueble = Inmueble.objects.get(pk=pk)

        user = self.request.user
        comentario_queryset = Comentario.objects.filter(
            inmueble=inmueble, comentario_user=user)

        if comentario_queryset.exists():
            raise ValidationError("El usuario ya comentado esta inmueble")

        inmueble.number_calificacion = (inmueble.number_calificacion + 1)
        inmueble.avg_calificacion = (
            serializer.validated_data['calificacion'] + inmueble.avg_calificacion) / inmueble.number_calificacion
        inmueble.save()

        serializer.save(inmueble=inmueble, comentario_user=user)


class Comentario_List(generics.ListCreateAPIView):
    serializer_class = ComentarioSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comentario_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comentario.objects.filter(inmueble=pk)


class Comentario_Detalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializers
    permission_classes = [IsAuthenticated, IsComentarioUserOrReadOnly]


"""
class Comentario_List(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Comentario_Detalle(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
"""
