

class SuppliersSettings(object):

    @property
    def INSTALLED_APPS(self):
        apps = super().INSTALLED_APPS + [
            'suppliers',
            'supplier_products'
        ]

        if 'ordered_model' not in apps:
            apps.append('ordered_model')

        return apps
