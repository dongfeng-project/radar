import copy
import logging

from dnslib import RR, QTYPE, RCODE
from dnslib.server import DNSServer, BaseResolver, DNSLogger

from radar.settings import DOMAIN, NS_SERVER

logger = logging.getLogger(__name__)


class MyLogger(DNSLogger):
    def log_data(self, dnsobj):
        pass

    def log_error(self, handler, e):
        pass

    def log_pass(self, *args):
        pass

    def log_prefix(self, handler):
        pass

    def log_recv(self, handler, data):
        pass

    def log_reply(self, handler, reply):
        pass

    def log_request(self, handler, request):
        domain = request.q.qname.__str__()

        if DOMAIN not in domain:
            return

        logger.info(f"收到域名解析请求 {domain}")

    def log_send(self, handler, data):
        pass

    def log_truncated(self, handler, reply):
        pass


class ZoneResolver(BaseResolver):
    def __init__(self, zone, glob=False):
        self.zone = [(rr.rname, QTYPE[rr.rtype], rr) for rr in RR.fromZone(zone)]
        self.glob = glob
        self.eq = "matchGlob" if glob else "__eq__"

    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        for name, rtype, rr in self.zone:
            # Check if label & type match
            if getattr(qname, self.eq)(name) and (qtype == rtype or qtype == "ANY" or rtype == "CNAME"):
                # If we have a glob match fix reply label
                if self.glob:
                    a = copy.copy(rr)
                    a.rname = qname
                    reply.add_answer(a)
                else:
                    reply.add_answer(rr)
                # Check for A/AAAA records associated with reply and
                # add in additional section
                if rtype in ["CNAME", "NS", "MX", "PTR"]:
                    for a_name, a_rtype, a_rr in self.zone:
                        if a_name == rr.rdata.label and a_rtype in ["A", "AAAA"]:
                            reply.add_ar(a_rr)
        if not reply.rr:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply


def main():
    """
    主函数
    :return:
    """
    zone = f"*.{DOMAIN}.       IN      A       {NS_SERVER}"

    resolver = ZoneResolver(zone, True)
    dns_logger = MyLogger()
    logger.info("启动域名解析 %s:%d" % ("0.0.0.0", 53))
    udp_server = DNSServer(resolver, port=53, address="0.0.0.0", logger=dns_logger)

    try:
        udp_server.start()
    except KeyboardInterrupt:
        logger.info("正在关闭域名解析……")
        udp_server.stop()
        logger.info("关闭域名解析完成")


if __name__ == "__main__":
    main()
