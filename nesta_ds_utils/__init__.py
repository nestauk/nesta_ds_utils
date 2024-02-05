from nesta_ds_utils.loading_saving import _gis_enabled, _excel_backend_available

feature_enabled = {
    "gis": _gis_enabled,
    "excel": _excel_backend_available,
}
