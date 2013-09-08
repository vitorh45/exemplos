from django.contrib.sitemaps import GenericSitemap
from django.conf import settings

from datetime import datetime, date

SITEMAP_LIMIT = getattr(settings, 'SITEMAP_LIMIT', 2000)

class LimitedSitemap(GenericSitemap):
    limit = SITEMAP_LIMIT
