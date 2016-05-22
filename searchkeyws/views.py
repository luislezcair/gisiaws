# -*- coding: utf-8 -*-

import subprocess
from rest_framework import viewsets
from rest_framework.response import Response
from searchkeyws.models import WSRequest, WSResponse, WSFilteredUrlsRequest, WSRequestState
from searchkeyws.serializers import WSRequestSerializer, WSResponseSerializer, WSFilteredUrlsRequestSerializer, WSRequestStateSerializer
from get_urls.search import obtener_urls

class WSResponseViewSet(viewsets.ModelViewSet):
    queryset = WSResponse.objects.all()
    serializer_class = WSResponseSerializer


class WSRequestViewSet(viewsets.ModelViewSet):
    queryset = WSRequest.objects.all()
    serializer_class = WSRequestSerializer

    def create(self, request, *args, **kwargs):
        wsrequest = WSRequestSerializer(data=request.data)
        response = { "status": "Invalid data" }

        if wsrequest.is_valid():
            request_object = wsrequest.save()

            data = wsrequest.validated_data
            json_respuesta = obtener_urls(data)

            # Agrega el id_request a la respuesta
            json_respuesta['id_request'] = request_object.id
            serializer = WSResponseSerializer(data=json_respuesta)

            if serializer.is_valid():
                response = serializer.data
            else:
                response = { "status": "Invalid response from search engine" }
        return Response(data=response)


class WSFilteredUrlsRequestViewSet(viewsets.ModelViewSet):
    queryset = WSFilteredUrlsRequest.objects.all()
    serializer_class = WSFilteredUrlsRequestSerializer

    def create(self, request, *args, **kwargs):
        r = WSFilteredUrlsRequestSerializer(data=request.data)

        if r.is_valid():
            request_object = r.save()

            subprocess.Popen(['python', 'webminer/webMiner.py', '-r' , str(request_object.request.id)])

        return Response(data={ "status": "ok" } )


class WSRequestStateViewSet(viewsets.ModelViewSet):
    queryset = WSRequestState.objects.all()
    serializer_class = WSRequestStateSerializer

