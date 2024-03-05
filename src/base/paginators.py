from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class FeedPagination(PageNumberPagination):
    page_size = settings.FEED_PAGE_SIZE


class FollowerPagination(PageNumberPagination):
    page_size = settings.FOLLOWER_PAGE_SIZE
