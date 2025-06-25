from rest_framework.pagination import PageNumberPagination


class HotelPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    page_size_size = 100