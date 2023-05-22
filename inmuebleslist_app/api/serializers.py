from rest_framework import serializers
from inmuebleslist_app.models import Inmueble, Tienda, Comentario


class ComentarioSerializers(serializers.ModelSerializer):

    comentario_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comentario
        exclude = ['inmueble']
        # fields = "__all__"


class InmuebleSerializers(serializers.ModelSerializer):

    comentarios = ComentarioSerializers(many=True, read_only=True)
    empresa_nombre = serializers.CharField(source='tienda.nombre')
    # longuitud_direccion = serializers.SerializerMethodField()

    class Meta:
        model = Inmueble
        fields = "__all__"
        # fields = ['id' , 'pais'] --> cuales quiero
        # exclude = ['id'] --> cuales no quiere

    def get_longuitud_direccion(self, data):
        cantidad = len(data.direccion)
        return cantidad

    def validate(self, data):
        if data['direccion'] == data['pais']:
            raise serializers.ValidationError(
                'La direcion y el pais deben ser diferentes')
        else:
            return data

    def validate_direccion(self, data):
        if len(data) < 6:
            raise serializers.ValidationError(
                'La direccion es demaciado corta')
        else:
            return data

    def validate_pais(self, data):
        if len(data) < 2:
            raise serializers.ValidationError(
                'El nombre del pais es demaciado corto')
        else:
            return data

    def validate_descripcion(self, data):
        if len(data) < 2:
            raise serializers.ValidationError(
                'La descripcion es demaciado corta')
        else:
            return data

    def validate_imagen(self, data):
        if len(data) < 2:
            raise serializers.ValidationError(
                'La URL de la imagen es demaciado corta')
        else:
            return data


class TiendaSerializers(serializers.ModelSerializer):
    # read_only=True -> solo lesctura
    inmuebleList = InmuebleSerializers(many=True, read_only=True)
    # inmuebleList = serializers.StringRelatedField(many=True)
    # inmuebleList = serializers.PrimaryKeyRelatedField(many=True , read_only=True)
    # inmuebleList = serializers.HyperlinkedRelatedField(
    #    many=True, read_only=True, view_name='inmueble-detalle')

    class Meta:
        model = Tienda
        fields = "__all__"
