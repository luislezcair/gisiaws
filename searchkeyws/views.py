from rest_framework import viewsets
from searchkeyws.models import WSRequest, WSResponse
from searchkeyws.serializers import WSRequestSerializer, WSResponseSerializer


class WSRequestViewSet(viewsets.ModelViewSet):
    queryset = WSRequest.objects.all()
    serializer_class = WSRequestSerializer


class WSResponseViewSet(viewsets.ModelViewSet):
    queryset = WSResponse.objects.all()
    serializer_class = WSResponseSerializer
