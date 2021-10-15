from rest_framework import pagination
from rest_framework.response import Response


class CustomPaginationIdeas(pagination.PageNumberPagination):
    """
    custom (based on docs) next+previous = will be sent not as 2 separate  links
    but as object links:{next,prev}
    """
    page_size = 3
    max_page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'prev': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
