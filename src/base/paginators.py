from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class UserListPagination(PageNumberPagination):
    page_size = settings.USER_LIST_PAGE_SIZE
    page_size_query_param = "page_size"
