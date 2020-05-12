from rest_framework import serializers

from .models import DNSReq, HTTPReq


class DNSReqSerializer(serializers.ModelSerializer):
    """
    认证序列化
    """

    class Meta:
        model = DNSReq
        fields = "__all__"


class HTTPReqSerializer(serializers.ModelSerializer):
    """
    订阅源类型序列化
    """

    class Meta:
        model = HTTPReq
        fields = "__all__"
