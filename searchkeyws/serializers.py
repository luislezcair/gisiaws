from rest_framework import serializers
from searchkeyws.models import *


class SearchKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchKey
        fields = ('id', 'clave')


class SearchUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchUrl
        fields = ('url',)


class FilteredUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilteredUrl
        fields = ('orden', 'url')


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

    def create(self, validated_data):
        claves = validated_data.pop('claves')
        request = WSRequest.objects.create(**validated_data)

        for key in claves:
            SearchKey.objects.create(request=request, **key)

        return request


class WSResponseSerializer(serializers.ModelSerializer):
    buscadores = SearchResultSerializer(many=True)

    class Meta:
        model = WSResponse
        fields = ('id_proyecto', 'id_request', 'buscadores')

    def create(self, validated_data):
        buscadores = validated_data.pop('buscadores')
        wsreponse = WSResponse.objects.create(**validated_data)

        for buscador in buscadores:
            urls = buscador.pop('urls')
            result = SearchResult.objects.create(response=wsreponse, **buscador)

            for url in urls:
                SearchUrl.objects.create(searchresult=result, **url)

        return wsreponse


class WSFilteredUrlsRequestSerializer(serializers.ModelSerializer):
    urls = FilteredUrlSerializer(many=True)

    class Meta:
        model = WSFilteredUrlsRequest
        fields = ('id_proyecto', 'nombre_directorio', 'request', 'urls')

    def create(self, validated_data):
        urls = validated_data.pop('urls')
        request = WSFilteredUrlsRequest.objects.create(**validated_data)

        for url in urls:
            FilteredUrl.objects.create(request=request, **url)

        return request
