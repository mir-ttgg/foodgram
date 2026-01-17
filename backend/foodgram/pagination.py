from rest_framework import pagination


class StandartPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 1000
