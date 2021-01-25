from django.apps import apps
from django.contrib import admin


class ListAdminMixin(object):
    # noinspection PyProtectedMember
    def __init__(self, model, admin_site):
        exclude_fields = ['password']
        # get all field names to be display as columns in table format
        self.list_display = [field.name for field in model._meta.fields if field.name not in exclude_fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


def register_app_models_to_admin_site(app_name, custom_admin_cls=dict()):
    models = apps.get_app_config(app_name).get_models()
    for model, model_admin in custom_admin_cls.items():
        admin.site.register(model, model_admin)
    for model in models:
        if model in custom_admin_cls:
            continue
        admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
        try:
            admin.site.register(model, admin_class)
        except admin.sites.AlreadyRegistered:
            pass
