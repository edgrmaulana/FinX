from django.utils.translation import gettext_lazy as _


SERVICE_CHOICES = (
    ("los", _("Loan Origination System")),
    ("crowdfunding", _("Crowdfunding")),
    ("disbursement", _("Disbursement")),
)

PERMISSION_MODEL_CHOICE = (
    ("project", "Project"),
    ("role", "Role"),
    ("company", "Company"),
    ("project_member", "Project Member"),
    ("user", "User"),
)
