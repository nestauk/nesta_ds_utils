try:
    from json import loads as load_json
    from geopandas import GeoDataFrame
    from io import BytesIO
    from fnmatch import fnmatch

    _gis_enabled = True

    def _gdf_to_fileobj(df_data: GeoDataFrame, path_to: str, **kwargs) -> BytesIO:
        """Convert GeoDataFrame into bytes file object.

        Args:
            df_data (gpd.DataFrame): Dataframe to convert.
            path_to (str): Saving file name.

        Returns:
            io.BytesIO: Bytes file object.
        """
        buffer = BytesIO()
        if fnmatch(path_to, "*.geojson"):
            df_data.to_file(buffer, driver="GeoJSON", **kwargs)
        else:
            raise NotImplementedError(
                "Uploading geodataframe currently supported only for 'geojson'."
            )
        buffer.seek(0)
        return buffer

    def _fileobj_to_gdf(fileobj: BytesIO, path_from: str, **kwargs) -> GeoDataFrame:
        """Convert bytes file object into geodataframe.

        Args:
            fileobj (io.BytesIO): Bytes file object.
            path_from (str): Path of loaded data.

        Returns:
            gpd.DataFrame: Data as geodataframe.
        """
        if fnmatch(path_from, "*.geojson"):
            return GeoDataFrame.from_features(
                load_json(fileobj.getvalue().decode())["features"]
            )

except ImportError:
    _gis_enabled = False
