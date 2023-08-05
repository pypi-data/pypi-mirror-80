
from django.apps import AppConfig, apps
from django.utils.translation import ugettext_lazy as _


class SuppliersAppConfig(AppConfig):

    name = 'suppliers'
    verbose_name = _('Suppliers')

    def ready(self):
        if not apps.is_installed('ckeditor'):
            raise Exception('`ckeditor` app is required for `suppliers`')


default_app_config = 'suppliers.SuppliersAppConfig'
