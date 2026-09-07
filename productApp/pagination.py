from rest_framework.pagination import PageNumberPagination, CursorPagination

class customPagination(PageNumberPagination):
    page_query_param = 'pg'
    page_size_query_param = 'size'

class customCursorPagination(CursorPagination):
    ordering = "created_at"