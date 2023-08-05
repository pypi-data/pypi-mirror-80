
from suit.sortables import SortableTabularInline

from suppliers.models import SupplierWarehouse


class SupplierWarehouseInline(SortableTabularInline):
    readonly_fields = ['price_updated']
    model = SupplierWarehouse
    extra = 0
    max_num = 100
