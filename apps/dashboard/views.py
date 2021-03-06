from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import DNSReq, HTTPReq
from .serializers import DNSReqSerializer, HTTPReqSerializer


# Create your views here.
class DNSReqViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    订阅源分类
    """

    queryset = DNSReq.objects.all().order_by("-updated")
    serializer_class = DNSReqSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
    )


class HTTPReqViewSet(viewsets.ModelViewSet):
    """
    订阅源
    """

    queryset = HTTPReq.objects.all().order_by("-updated")
    serializer_class = HTTPReqSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
    )
