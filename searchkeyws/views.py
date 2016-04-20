# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.response import Response
from searchkeyws.models import WSRequest, WSResponse, WSFilteredUrlsRequest
from searchkeyws.serializers import WSRequestSerializer, WSResponseSerializer, WSFilteredUrlsRequestSerializer


class WSResponseViewSet(viewsets.ModelViewSet):
    queryset = WSResponse.objects.all()
    serializer_class = WSResponseSerializer

    # def create(self, request, *args, **kwargs):
    #     wsresponse = WSResponseSerializer(data=request.data)

    #     if wsresponse.is_valid():
    #         wsresponse.save()

    #         data = wsresponse.validated_data


class WSRequestViewSet(viewsets.ModelViewSet):
    queryset = WSRequest.objects.all()
    serializer_class = WSRequestSerializer

    def create(self, request, *args, **kwargs):
        wsrequest = WSRequestSerializer(data=request.data)

        if wsrequest.is_valid():
            wsrequest.save()

            data = wsrequest.validated_data

            # Si la solicitud es válida, los datos están en data
            # Acá se podría lanzar el proceso de obtención de URLs con las claves.
            print("id_proyecto: ", data['id_proyecto'])
            print("nombre_directorio", data['nombre_directorio'])

            for i, c in enumerate(data['claves']):
                print("Clave %d: " % i, c['clave'])

        # Devuelve una respuesta válida para probar la comunicación
        response = WSResponse.objects.all().last()
        serializer = WSResponseSerializer(response)
        return Response(data=serializer.data)


class WSFilteredUrlsRequestViewSet(viewsets.ModelViewSet):
    queryset = WSFilteredUrlsRequest.objects.all()
    serializer_class = WSFilteredUrlsRequestSerializer

    def create(self, request, *args, **kwargs):
        r = WSFilteredUrlsRequestSerializer(data=request.data)

        if r.is_valid():
            r.save()

            data = r.validated_data

            # Si la solicitud es válida, los datos están en data
            # Acá se podría lanzar el proceso de minería con las URLS filtradas.
            print("id_proyecto: ", data['id_proyecto'])
            print("nombre_directorio", data['nombre_directorio'])

            for url in data['urls']:
                print("Orden: %d" % url['orden'])
                print("URL: %s" % url['url'])

        return Response(data={"status": "ok"})
