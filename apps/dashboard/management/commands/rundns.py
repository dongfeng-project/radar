from django.core.management.base import BaseCommand, CommandError

import dns.server


class Command(BaseCommand):
    help = "Run DNS Server."

    def handle(self, *args, **options):
        try:
            dns.server.main()
        except Exception as e:
            raise CommandError(f"Unhandled error occurred when running DNS server {e}")
