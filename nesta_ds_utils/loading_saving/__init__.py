from nesta_ds_utils.loading_saving.gis_interface import _gis_enabled

try:
    import openpyxl

    _excel_backend_available = True

except ImportError:
    _excel_backend_available = False
