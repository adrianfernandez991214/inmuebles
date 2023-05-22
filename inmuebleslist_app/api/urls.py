from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inmuebleslist_app.api.views import (Inmueble_listAV, Inmueble_detalleAV, Tienda_listAV,
                                         Tienda_detalleAV, Comentario_List, Comentario_Detalle, Cometario_Create,
                                         TiendaVS, UsuarioComentario, Inmueble_lista_filter)


router = DefaultRouter()
router.register('tienda', TiendaVS, basename='tienda')

urlpatterns = [
    # path('tienda/list/', Tienda_listAV.as_view(), name='tienda-list'),
    # path('tienda/<int:pk>/', Tienda_detalleAV.as_view(), name='tienda-detalle'),

    path('', include(router.urls)),

    path('inmueble/', Inmueble_listAV.as_view(), name='inmueble-list'),
    path('inmueble/list/', Inmueble_lista_filter.as_view(),
         name='inmueble-list-filter'),
    path('inmueble/<int:pk>/', Inmueble_detalleAV.as_view(),
         name='inmueble-detalle'),

    path('inmueble/<int:pk>/comentario-create/',
         Cometario_Create.as_view(), name='comentario-create'),
    path('inmueble/<int:pk>/comentario/',
         Comentario_List.as_view(), name='comentario-list'),
    path('inmueble/comentario/<int:pk>/', Comentario_Detalle.as_view(),
         name='comentario-detalle'),
    # path('inmueble/comentario/<str:username>/', UsuarioComentario.as_view(),
    #    name='usuario-comentario-detalle'),

    path('inmueble/comentario/', UsuarioComentario.as_view(),
         name='usuario-comentario-detalle'),

]
