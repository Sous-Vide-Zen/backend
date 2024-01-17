from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class FeedPagination(PageNumberPagination):
    page_size = settings.FEED_PAGE_SIZE
