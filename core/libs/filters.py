import coreapi
from rest_framework.filters import SearchFilter


class ProvinceIDFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="province_id",
                location="query",
                required=True,
                type="string",
                description="filter by province id",
            )
        ]


class RegencyIDFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="regency_id",
                location="query",
                required=True,
                type="string",
                description="filter by regency id",
            )
        ]


class DistrictIDFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="district_id",
                location="query",
                required=True,
                type="string",
                description="filter by district id",
            )
        ]


class ProjectIDFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="project_id62",
                location="query",
                required=False,
                type="string",
                description="filter by project_id62",
            )
        ]
