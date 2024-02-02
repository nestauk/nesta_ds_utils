try:
    import openpyxl

    _excel_backend_available = True

except ImportError:
    _excel_backend_available = False
