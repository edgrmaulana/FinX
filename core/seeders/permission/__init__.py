from core.structures.role.models import Permission
from core.libs.constants import PERMISSION_MODEL_CHOICE


def generate_permissions():
    actions = ["view", "add", "change", "delete"]
    for model in PERMISSION_MODEL_CHOICE:
        model_name = model[0]
        for action in actions:
            name = f"Can {action} {model_name}"
            code_name = f"{action}_{model_name}"

            kwargs_to_query = {
                "name": name,
                "code_name": code_name,
                "content_type_model": model_name,
            }
            permission = Permission.objects.filter(**kwargs_to_query).last()
            if not permission:
                Permission.objects.create(**kwargs_to_query)
