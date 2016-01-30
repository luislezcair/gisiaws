from rest_framework import viewsets
from searchkeyws.models import WSRequest, WSResponse, WSFilteredUrlsRequest
from searchkeyws.serializers import WSRequestSerializer, WSResponseSerializer, WSFilteredUrlsRequestSerializer


class WSRequestViewSet(viewsets.ModelViewSet):
    queryset = WSRequest.objects.all()
    serializer_class = WSRequestSerializer


class WSResponseViewSet(viewsets.ModelViewSet):
    queryset = WSResponse.objects.all()
    serializer_class = WSResponseSerializer


class WSFilteredUrlsRequestViewSet(viewsets.ModelViewSet):
    queryset = WSFilteredUrlsRequest.objects.all()
    serializer_class = WSFilteredUrlsRequestSerializer
