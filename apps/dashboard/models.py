from django.db import models

from utils.models import BaseModel


# Create your models here.
class DNSReq(BaseModel):
    """
    DNS请求
    """

    domain = models.CharField(verbose_name="请求地址", max_length=1024, default="", db_index=True)

    class Meta:
        verbose_name = "DNS请求"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.domain


class HTTPReq(BaseModel):
    """
    HTTP请求记录
    """

    url = models.URLField(verbose_name="URL", db_index=True)
    referer = models.CharField(verbose_name="Referer", max_length=1024, default="")
    sip = models.GenericIPAddressField(verbose_name="来源IP", default="")
    ua = models.CharField(verbose_name="User-Agent", max_length=256, default="")

    class Meta:
        verbose_name = "HTTP请求"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.url}"


def save_dns_req(domain: str):
    """
    保存DNS解析请求
    :param domain:
    :return:
    """
    dns_req_obj = DNSReq(domain=domain)
    dns_req_obj.save()


def save_http_req(url: str, referer: str, sip: str, ua: str):
    """
    保存HTTP请求
    :param url:
    :param referer:
    :param sip:
    :param ua:
    :return:
    """
    http_req_obj = HTTPReq(url=url, referer=referer, sip=sip, ua=ua)
    http_req_obj.save()
