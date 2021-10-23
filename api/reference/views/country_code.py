import json
import os
from django.conf import settings

from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter
from enterprise.libs.rest_module.response import DRFResponse


class CountryCodeViewSet(GenericViewSet):
    filter_backends = (SearchFilter,)

    def list(self, request):
        json_path = os.path.join(
            settings.BASE_DIR, "core/data_constants/data_country_code.json"
        )
        data_response = []
        with open(json_path) as f:
            data = json.load(f)
            for d in data:
                if not d.get("dial_code"):
                    continue

                data_response.append(
                    {
                        "dial": d.get("dial_code"),
                        "id": d.get("code"),
                        "name": d.get("name"),
                        "flag": d.get("flag")
                    }
                )

        search_params = self.request.query_params.get("search")
        if search_params:
            search_params_lower = search_params.lower()
            data_response = [item for item in data_response if search_params_lower in item["name"].lower() ]

        response = DRFResponse(
            {
                "en": "Success fetching data",
                "id": "Berhasil mengambil data",
            }
        )
        return response.get_success_response("200", data_response)
