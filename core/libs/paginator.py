from rest_framework import pagination


class DRFPagination(pagination.LimitOffsetPagination):
    def get_paginated_response_dict(self, data):
        response = dict()
        response["count"] = self.count
        response["next"] = self.get_next_link()
        response["previous"] = self.get_previous_link()
        response["results"] = data

        return response
