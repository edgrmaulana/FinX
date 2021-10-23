from core.structures.company.models import Company
from enterprise.structures.administrative.models import Address


class CompanyManager(object):
    model_class = Company

    def create(self, *args, **kwargs):
        address = kwargs.pop("address", None)
        created_by = kwargs.get("created_by")

        if address:
            address = Address.objects.create(**address, created_by=created_by)
            kwargs["address"] = address

        return self.model_class.objects.create(**kwargs)

    def list(self, **kwargs):
        return self.model_class.objects.filter(deleted_at__isnull=True, **kwargs)

    def get_company(self, **kwargs):
        return self.model_class.objects.filter(**kwargs).last()

    def update(self, id62, **kwargs):
        company = self.model_class.objects.filter(id62=id62)

        address_instance = company.last().address if company.last() else None
        address_kwargs = kwargs.get("address")

        company.update(
            display_name=kwargs.get("display_name"),
            business_type=kwargs.get("business_type"),
            description=kwargs.get("description"),
            website=kwargs.get("website"),
        )

        if address_instance and address_kwargs:
            Address.objects.filter(id62=address_instance.id62).update(**address_kwargs)

        if not address_instance and address_kwargs:
            address_instance = Address.objects.create(
                **address_kwargs, created_by=company.owned_by
            )
            company.address = address_instance
            company.save()

    def delete(self, id):
        Company.objects.filter(id62=id).delete()
