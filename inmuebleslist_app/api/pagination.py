from rest_framework.pagination import LimitOffsetPagination


class InmuebleLOPagination(LimitOffsetPagination):
    default_limit = 1
