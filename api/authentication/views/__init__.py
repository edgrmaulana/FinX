from django.views.generic import TemplateView
from django.conf import settings


class IndexView(TemplateView):
    template_name = "oauth/index.html"
    is_index_page = True

    def get(self, request):
        client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
        return self.render_to_response({"client_id": client_id})
