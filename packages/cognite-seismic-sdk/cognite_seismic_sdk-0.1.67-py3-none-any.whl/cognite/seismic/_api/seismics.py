import os
from typing import *

from cognite.seismic._api.api import API
from cognite.seismic._api.utility import LineRange, MaybeString, Metadata, get_identifier, get_search_spec
from google.protobuf.struct_pb2 import Struct
from google.protobuf.wrappers_pb2 import Int32Value as i32
from google.protobuf.wrappers_pb2 import StringValue

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import (
        SearchSeismicsRequest,
        CreateSeismicRequest,
        EditSeismicRequest,
        DeleteSeismicRequest,
        DeleteSeismicResponse,
        VolumeRequest,
    )
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import Seismic, OptionalMap, Identifier
    from cognite.seismic.protos.types_pb2 import Geometry as GeometryProto, Wkt, GeoJson
else:
    from cognite.seismic._api.shims import Seismic, Geometry as GeometryProto, Identifier


class VolumeDef:
    def __init__(self, volumedef: str):
        self.volumedef = volumedef


class Geometry:
    """Represents a CRS + shape, in either a WKT format or a GeoJSON."""

    def __init__(self, crs: str, *, geojson: Union[Struct, None] = None, wkt: Union[str, None] = None):
        if (geojson is None) and (wkt is None):
            raise Exception("You must specify one of: geojson, wkt")
        if (geojson is not None) and (wkt is not None):
            raise Exception("You must specify either of: geojson, wkt")
        self.crs = crs
        self.geojson = geojson
        self.wkt = wkt

    def to_proto(self):
        geometry = GeometryProto(crs=self.crs)
        if self.geojson is not None:
            geometry.geojson = GeoJson(json=self.geojson)
        if self.wkt is not None:
            geometry.wkt = Wkt(geometry=self.wkt)
        return geometry


class SeismicAPI(API):
    def __init__(self, query, ingestion, metadata):
        super().__init__(query=query, ingestion=ingestion, metadata=metadata)

    def create(
        self,
        *,
        external_id: str,
        name: MaybeString = None,
        partition_identifier: Union[int, str],
        seismic_store_id: str,
        volumedef: Union[str, None] = None,
        geometry: Union[Geometry, None] = None,
        metadata: Union[Metadata, None] = None,
    ) -> Seismic:
        """Create a new Seismic.
        
        If neither volumedef nor geometry are specified, the new Seismic will be able to access the entire seismic store it is derived from.

        Args:
            externaL_id (str): The external id of the new Seismic
            name (str | None): (Optional) If specified, the name of the new Seismic
            partition_identifier (int | str): Either the partition id or external_id that the Seismic is part of
            seismic_store_id (str): The seismic store that the new Seismic is derived from
            volumedef (str | None): (Optional) If specified, uses a VolumeDef as the shape of the Seismic
            geometry (Geometry | None): (Optional) If specified, uses a Geometry (either a WKT or GeoJson) as the shape of the Seismic

        Returns:
            Seismic: The newly created Seismic with minimal data. Use search() to retrieve all data.
        """
        if type(partition_identifier) == int:
            identifier = Identifier(id=str(partition_identifier))
        elif type(partition_identifier) == str:
            identifier = Identifier(external_id=partition_identifier)
        else:
            raise Exception("partition_identifier should be an int or a str.")

        request = CreateSeismicRequest(external_id=external_id, partition=identifier, seismic_store_id=seismic_store_id)
        if volumedef is not None:
            request.volume_def.MergeFrom(volumedef)
        elif geometry is not None:
            request.geometry.MergeFrom(geometry.to_proto())

        if name is not None:
            request.name = name

        if metadata is not None:
            request.metadata = OptionalMap(data=metadata)

        return self.query.CreateSeismic(request, metadata=self.metadata)

    def search(
        self,
        mode: str = "seismic",
        *,
        id: Union[int, None] = None,
        external_id: MaybeString = None,
        external_id_substring: MaybeString = None,
        name: MaybeString = None,
        name_substring: MaybeString = None,
        get_all: bool = False,
    ) -> Iterable[Seismic]:
        """Search for seismics.
        
        Can search all seismics included in surveys, partitions, or directly search seismics,
        specified by id, external_id, name, or substrings of external_id or name. 
        Only one search method should be specified. The behaviour when multiple are specified is undefined.

        Args:
            mode (str): One of "survey", "seismic" or "partition".
            id (int|None): id to search by
            external_id (str|None): external id to search by
            external_id_substring (str|None): Substring of external id to search by
            name (str|None): Name to search by
            name_substring (str|None): Substring of name to search by
            get_all (bool): Whether to instead retrieve all visible Seismic. Equivalent to list().
        
        Returns:
            Iterable[Seismic]: The list of matching Seismics
        """
        spec = get_search_spec(id, external_id, external_id_substring, name, name_substring)

        if get_all:
            req = SearchSeismicsRequest()
        else:
            if mode == "seismic":
                req = SearchSeismicsRequest(seismic=spec)
            elif mode == "survey":
                req = SearchSeismicsRequest(survey=spec)
            elif mode == "partition":
                req = SearchSeismicsRequest(partition=spec)
            else:
                raise Exception("mode should be one of: survey, seismic, partition")

        return self.query.SearchPartitions(req, metadata=self.metadata)

    def edit(
        self,
        *,
        id: Union[int, None] = None,
        external_id: MaybeString = None,
        name: MaybeString = None,
        metadata: Union[Metadata, None] = None,
    ):
        """Edit an existing seismic.
        
        Either the id or the external_id should be provided in order to identify the seismic.
        The editable fields are name and metadata. Providing a name or metadata field will replace the existing data with the new data. Providing an empty string as the name will delete the seismic name.
        
        Args:
            id (int | None): The id of the seismic
            external_id (str | None): The external id of the seismic
            name (str | None): (Optional) The new name of the seismic
            metadata (Dict[str, str] | None): (Optional) The new metadata for the seismic
        
        Returns:
            Seismic: The edited Seismic with minimal data. Use search() to retrieve all data.
        """
        identifier = get_identifier(id, external_id)
        request = EditSeismicRequest(identifier=identifier)
        if name is not None:
            request.name = StringValue(value=name)
        if metadata is not None:
            request.metadata = OptionalMap(data=metadata)

        return self.query.EditSeismic(request, metadata=self.metadata)

    def delete(self, *, id: Union[int, None] = None, external_id: MaybeString = None):
        """Delete a seismic

        Either the id or the external id should be provided in order to identify the seismic.
        
        Args:
            id (int | None): The id of the seismic
            external_id (str | None): The external id of the seismic
        
        Returns:
            bool: True if successful
        """
        identifier = get_identifier(id, external_id)
        request = DeleteSeismicRequest(seismic=identifier)

        return self.query.DeleteSeismic(request, metadata=self.metadata).succeeded
