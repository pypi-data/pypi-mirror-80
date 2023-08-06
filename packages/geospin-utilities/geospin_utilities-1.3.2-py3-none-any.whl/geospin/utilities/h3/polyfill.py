"""A set of extensions for the h3 PolyFiller."""
try:
    import h3

    h3.k_ring('841e265ffffffff', 4)
except AttributeError:
    from h3 import h3

import logging
import time

import pyproj
import shapely
import shapely.ops
import shapely.wkt

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def buffer_polygon(polygon, buffer_size,
                   source_crs='epsg:4326',
                   buffering_crs='epsg:3035'):
    """
    Create a buffer around the given polygon and return it.

    :param shapely.geometry.Polygon polygon: A polygon
    :param int buffer_size: Size of the buffer in meters
    :param str source_crs: Source CRS of the polygon
    :param str buffering_crs: CRS used to calculate the buffer. Must
        be metric, measured in meter. Will not be checked!
    :return shapely.geometry.Polygon poly:
        The buffered polygon
    """
    # transform to metric crs
    # https://gis.stackexchange.com/questions/127427/transforming-shapely
    # -polygon-and-multipolygon-objects
    projection = pyproj.Transformer.from_proj(
        pyproj.Proj(init=source_crs),
        pyproj.Proj(init=buffering_crs)
    )
    polygon_metric = shapely.ops.transform(projection.transform, polygon)
    # add buffer
    # https://gis.stackexchange.com/questions/97963/how-to-surround-a-polygon
    # -object-with-a-corridor-of-specified-width/97964
    polygon_metric = polygon_metric.buffer(distance=buffer_size)
    # transform back to origin crs
    projection = pyproj.Transformer.from_proj(
        pyproj.Proj(init=buffering_crs),
        pyproj.Proj(init=source_crs)
    )
    poly = shapely.ops.transform(projection.transform, polygon_metric)
    return poly


class PolyFiller:
    """
    Fill polygons and multipolygons with H3 hexagons.

    This extends upon H3's ``polyfill`` function in the following ways:
    * Geometries can be specified in different formats
    * Multipolygons are supported
    * Whether or not hexagons at the geometry boundaries are included or
    excluded can be specified

    .. note::
        If geometry is a single polygon in GeoJSON format and no buffering is
        desired one can use `polyfill` from H3 directly (more efficient,
        because no shape transformation is required).
    """

    def __init__(self,
                 resolution=9,
                 add_hex_id_if='center_within_buffer',
                 source_crs='epsg:4326',
                 buffer_crs='epsg:3035'):
        """
        :param int resolution:
            Resolution of H3 hexagons that should fill the polygon
        :param str add_hex_id_if:
            Choose 'center_within_buffer' or 'center_contained'.

            For 'center_contained', only hex IDs whose centers are within the
            provided geometry are returned by `fill()`.

            For 'center_within_buffer', a buffer is added to the geometry that
            is to be filled. This buffer is slightly smaller than the average
            distance between two centers. Note that the distance between two
            centers is different at different locations because the sizes of
            H3 hexagons vary. If the distance were constant, it would
            suffice to choose the buffer size equal to the edge length. Here
            we make it `1.73 x edge length`. The rationale is this: Making it
            larger leads to less hex IDs that are missed. Making it smaller
            than `sqrt(3) x edge length` avoids adding too many hex IDs that
            are outside the given polygons. However, this does not guarantee
            that no hex IDs are missed if the edge length varies by more than
            1.73 in the area of the provided geometries. Neither does it
            guarantee that no unnecessary hexagons are added at the boundary
            (indeed, this is very likely to happen).

        :param str source_crs:
            Coordinate reference system of `geometry`. Not needed,
            if `geometry` is a GeoJson dictionary
        :param str buffer_crs:
            Coordinate reference system used for buffering. The default 3035 is
            accurate in Europe.
        """
        self.resolution = resolution
        self.add_hex_id_if = add_hex_id_if
        self.source_crs = source_crs
        self.buffer_crs = buffer_crs

    def fill(self, geometry):
        """
        Return list of hex IDs that are inside `geometry`.

        :param geometry:
            Representation of a polygon or a multipolygon. This can either be a
            GeoJson dictionary, a WKT string or a shapely geometry.
        :type geometry:
            dict or str or shapely.geometry.Polygon or
            shapely.geometry.MultiPolygon
        :return list: List of H3 hex IDs.
        """
        hex_ids = []
        polygons = self._get_list_of_polygons_in_geometry(geometry)
        for polygon in polygons:
            hex_ids.extend(self._fill_polygon(polygon))
        return list(set(hex_ids))

    def _fill_polygon(self, polygon):
        """
        :param shapely.geometry.Polygon polygon:
        :return list:
            List of hex IDs inside ``polygon``
        """
        # Convert shapely object to geojson
        geo_json = shapely.geometry.mapping(polygon)
        hex_ids = h3.polyfill(geo_json, res=self.resolution,
                              geo_json_conformant=True)
        return hex_ids

    def _buffer_polygon(self, polygon):
        """
        Apply different buffering schemes specified by `self.add_hex_id_if`.

        :param shapely.geometry.Polygon polygon:
        :return shapely.geometry.Polygon buffered_polygon:
            A buffered polygon
        """
        if self.add_hex_id_if == 'center_within_buffer':
            buffer_size = 1.73 * h3.edge_length(self.resolution, 'm')
            buffered_polygon = buffer_polygon(
                polygon, buffer_size, source_crs=self.source_crs,
                buffering_crs=self.buffer_crs)
        elif self.add_hex_id_if == 'contained':
            raise NotImplementedError
        else:
            raise ValueError('Buffering scheme not known.')

        return buffered_polygon

    @staticmethod
    def _convert_geometry_to_shape(geometry):
        """
        :return shape.geometry.base.BaseGeometry:
            Shapely geometry based on representation specified in `geometry`.
            See `fill()` for details.
        """
        if isinstance(geometry, str):
            shape = shapely.wkt.loads(geometry)
        elif isinstance(geometry, dict):
            shape = shapely.geometry.asShape(geometry)
        elif isinstance(geometry, shapely.geometry.base.BaseGeometry):
            # No conversion for shapely geometries
            shape = geometry
        else:
            raise ValueError('Geometry is in invalid format.')
        return shape

    def _get_list_of_polygons_in_geometry(self, geometry):
        """
        :return list: List of shapely Polygons that comprise `geometry`
        """
        shape = PolyFiller._convert_geometry_to_shape(geometry)

        # 'center-contained' does not require buffering
        if self.add_hex_id_if == 'center_contained':
            shape = shape
        elif self.add_hex_id_if == 'center_within_buffer':
            shape = self._buffer_polygon(shape)
        else:
            raise NotImplementedError(
                f"Method '{self.add_hex_id_if}' not implemented")

        if isinstance(shape, shapely.geometry.Polygon):
            polygons = [shape]
        elif isinstance(shape, shapely.geometry.MultiPolygon):
            polygons = shape
        else:
            raise ValueError('shape must be Polygon or MultiPolygon')
        return polygons


class RoadNetworkPolyFiller:
    """
    Fill geometry with H3 hexagons that are close to roads.

    This is an extension of the h3 polyfill function that fills only areas
    which are within a buffer around the road network.

    Note: The road network is extracted from a PostgreSQL database which is
        created using `osm2pqsql`.

    :param geospin.utilities.backend.DatabaseBackend osm_db_backend: The backend
        to the OSM database containing the table `planet_osm_line`.
    :param int buffer_size: Buffer size to put around the road network (meters).
    :param int resolution: The H3 resolution.
    :param int chunk_resolution: The resolution of chunk hexagons (must be
        smaller or equal to `resolution`).
    """

    def __init__(self, osm_db_backend, buffer_size, resolution,
                 chunk_resolution=6):
        self.osm_db_backend = osm_db_backend
        self.buffer_size = buffer_size
        self.resolution = resolution
        self.chunk_resolution = chunk_resolution

        self.road_network_view_name = 'road_network'
        self.buffered_road_network_view_name = 'buffered_road_network'

    def fill(self, geometry):
        """
        Fill geometry with hexagons that are close to roads.

        The filling will be done in chunks: the geometry is sub-sampled into
        smaller areas by using H3 polyfill at a resolution that is lower than
        the fill resolution.

        Note: The area is fully covered but there will be hexagons extending
            beyond the bounds of the geometry.

        :param shapely.geometry.Polygon, shapely.geometry.MultiPolygon geometry:
            Geometry to fill.
        :return list(str) hex_ids: List of hex IDs.
        """
        chunk_hex_ids = self._get_chunk_hex_ids(geometry)
        n_chunks = len(chunk_hex_ids)
        logger.info(f'Found #{n_chunks} chunks.')
        self._create_road_network_view()

        hex_ids = set()
        for index, chunk_hex_id in enumerate(chunk_hex_ids, 1):
            logger.info(
                f'Start with ({index}/{n_chunks})...')
            start_time = time.time()

            hex_ids_in_chunk = list(
                h3.h3_to_children(chunk_hex_id, self.resolution))
            road_network_hex_ids_in_chunk = \
                self._filter_hex_ids_that_intersect_buffered_road_network(
                    hex_ids=hex_ids_in_chunk
                )
            hex_ids.update(road_network_hex_ids_in_chunk)
            logger.info(
                f'Found #{len(road_network_hex_ids_in_chunk)} matching hex IDs.'
                f'Done in {time.time() - start_time} sec.')

        self._drop_road_network_view()
        return list(hex_ids)

    def _create_road_network_view(self):
        """Create a view of the road network.

        The lines in the `planet_osm_lines` are filtered by comparing the
        highway and access values with a whitelist.
        """
        highway_whitelist = ['motorway', 'motorway_link', 'trunk',
                             'trunk_link', 'primary', 'primary_link',
                             'secondary', 'secondary_link', 'tertiary',
                             'tertiary_link', 'residential', 'living_street',
                             'unclassified', 'service', 'pedestrian']
        access_whitelist = ['yes', 'motorcar', 'motor_vehicle', 'vehicle',
                            'permissive', 'hov', 'delivery',
                            'destination', 'customers', 'private', 'psv',
                            'emergency']
        vehicle_whitelist = ['yes', 'private', 'permissive', 'destination']
        motor_vehicle_whitelist = ['yes', 'private', 'permissive',
                                   'destination']

        with self.osm_db_backend.engine.connect() as conn:
            sql = f"""CREATE OR REPLACE VIEW {self.road_network_view_name} AS
            (SELECT
                ol.way AS geom
            FROM
                STRING_TO_ARRAY('{';'.join(highway_whitelist)}', ';')
                    AS highway_whitelist,
                STRING_TO_ARRAY('{';'.join(access_whitelist)}', ';')
                    AS access_whitelist,
                STRING_TO_ARRAY('{';'.join(vehicle_whitelist)}', ';')
                    AS vehicle_whitelist,
                STRING_TO_ARRAY('{';'.join(motor_vehicle_whitelist)}', ';')
                    AS motor_vehicle_whitelist,
                planet_osm_line AS ol
            WHERE
                ol.highway = ANY(highway_whitelist)
                OR ol.access = ANY(access_whitelist)
                OR (exist(ol.tags, 'vehicle')
                    AND ol.tags->'vehicle' = ANY(vehicle_whitelist))
                OR (exist(ol.tags, 'motor_vehicle')
                    AND ol.tags->'motor_vehicle' = ANY(motor_vehicle_whitelist))
            )
            """
            conn.execute(sql)

    def _drop_road_network_view(self):
        with self.osm_db_backend.engine.connect() as conn:
            sql = f"DROP VIEW {self.road_network_view_name};"
            conn.execute(sql)

    def _filter_hex_ids_that_intersect_buffered_road_network(
            self, hex_ids):
        geometries = [self._hex_id_to_polygon(hex_id) for hex_id in hex_ids]

        geometry_wkts = [g.wkt for g in geometries]

        with self.osm_db_backend.engine.connect() as conn:
            sql = f"""
                WITH refs AS (
                  SELECT
                    elem.nr AS nr,
                    ST_Transform(ST_GeomFromText(elem.wkt, 4326), 3857) AS geom,
                    ST_Y(ST_Centroid(ST_GeomFromText(elem.wkt, 4326))) AS lat
                  FROM
                    UNNEST(STRING_TO_ARRAY('{';'.join(geometry_wkts)}', ';'))
                    WITH ORDINALITY AS elem(wkt, nr))
                SELECT
                    nr - 1
                FROM
                    refs AS rp
                INNER JOIN road_network AS rn
                ON ST_Dwithin(
                    rp.geom,
                    rn.geom,
                    {self.buffer_size} / cosd(rp.lat)
                    )
                """
            result = conn.execute(sql).fetchall()

        intersecting_idxs = [idx[0] for idx in result]
        intersecting_hex_ids = [hex_ids[i] for i in intersecting_idxs]

        return intersecting_hex_ids

    @staticmethod
    def _hex_id_to_polygon(hex_id):
        boundaries = h3.h3_to_geo_boundary(hex_id, True)
        return shapely.geometry.asPolygon(boundaries)

    def _get_chunk_hex_ids(self, geometry):
        """Return all the hex_ids given in the geometry."""
        chunker = PolyFiller(self.chunk_resolution,
                             add_hex_id_if='center_within_buffer')
        chunk_hex_ids = chunker.fill(geometry)
        return chunk_hex_ids
