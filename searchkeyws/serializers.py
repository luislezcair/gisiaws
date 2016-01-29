from rest_framework import serializers
from searchkeyws.models import WSRequest, WSResponse, SearchKey, SearchResult, SearchUrl


class SearchKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchKey
        fields = ('id', 'clave')


class SearchUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchUrl
        fields = ('url',)


class SearchResultSerializer(serializers.ModelSerializer):
    urls = SearchUrlSerializer(many=True)

    class Meta:
        model = SearchResult
        fields = ('buscador', 'urls')


class WSRequestSerializer(serializers.ModelSerializer):
    claves = SearchKeySerializer(many=True)

    class Meta:
        model = WSRequest
        fields = ('id_proyecto', 'nombre_directorio', 'claves')


class WSResponseSerializer(serializers.ModelSerializer):
    buscadores = SearchResultSerializer(many=True)

    class Meta:
        model = WSResponse
        fields = ('id_proyecto', 'buscadores')
