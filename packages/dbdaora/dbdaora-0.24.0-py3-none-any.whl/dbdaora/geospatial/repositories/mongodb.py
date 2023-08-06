from dbdaora.data_sources.fallback.mongodb import Key

from . import GeoSpatialRepository


class MongodbGeoSpatialRepository(GeoSpatialRepository[Key]):
    __skip_cls_validation__ = ('MongodbGeoSpatialRepository',)
    fallback_data_source_key_cls = Key
