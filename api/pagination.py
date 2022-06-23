from rest_framework.exceptions import NotFound, APIException
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.pagination import (
    PageNumberPagination as RestFrameworkPageNumberPagination,
)
from rest_framework.views import APIView


class PageNumberPagination(RestFrameworkPageNumberPagination):
    # Please keep the default page size in sync with the default prop pageSize in
    # web-frontend/modules/core/components/helpers/InfiniteScroll.vue
    page_size = 100
    page_size_query_param = "size"

    def __init__(self, limit_page_size=None, *args, **kwargs):
        self.limit_page_size = limit_page_size
        super().__init__(*args, **kwargs)

    def get_page_size(self, request):
        page_size = super().get_page_size(request)

        if self.limit_page_size and page_size > self.limit_page_size:
            exception = APIException(
                {
                    "error": "ERROR_PAGE_SIZE_LIMIT",
                    "detail": f"The page size is limited to {self.limit_page_size}.",
                }
            )
            exception.status_code = HTTP_400_BAD_REQUEST
            raise exception

        return page_size

    def paginate_queryset(self, *args, **kwargs):
        """Adds a machine readable error code if the page is not found."""

        try:
            return super().paginate_queryset(*args, **kwargs)
        except NotFound as e:
            exception = APIException({"error": "ERROR_INVALID_PAGE", "detail": str(e)})
            exception.status_code = HTTP_400_BAD_REQUEST
            raise exception


class PaginationAPIView(APIView):
    queryset = None
    serializer_class = None
    pagination_class = None

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        # assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'perpage'

    def get_paginated_response(self, data):
        response = Response(data)
        response['count'] = self.page.paginator.count
        response['current'] = self.page.number
        response['next'] = self.get_next_link()
        response['previous'] = self.get_previous_link()
        pagination = {
            'page': self.page.number,
            'total_page': self.page.paginator.num_pages,
            'total_row': self.page.paginator.count,
            'perpage': self.page.paginator.per_page
        }
        content = {
            'pagination': pagination,
            'data': data,
            'response_code': 200,
            'response_msg': 'SUCCESS'
        }
        return Response(content)


