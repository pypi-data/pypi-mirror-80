#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import Iterator, List, Optional

from psym.client import SymphonyClient
from psym.common.cache import LOCATION_TYPES
from psym.common.data_class import Location, LocationType, PropertyDefinition
from psym.common.data_enum import Entity
from psym.common.data_format import (
    format_to_location_type,
    format_to_property_type_inputs,
)

from ..exceptions import EntityNotFoundError
from ..graphql.input.add_location_type import AddLocationTypeInput
from ..graphql.mutation.add_location_type import AddLocationTypeMutation
from ..graphql.mutation.remove_location_type import RemoveLocationTypeMutation
from ..graphql.query.location_type_details import LocationTypeDetailsQuery
from ..graphql.query.location_type_locations import LocationTypeLocationsQuery
from ..graphql.query.location_types import LocationTypesQuery
from .location import delete_location


def _populate_location_types(client: SymphonyClient) -> None:
    location_types = LocationTypesQuery.execute(client)
    if not location_types:
        return
    edges = location_types.edges
    for edge in edges:
        node = edge.node
        if node:
            LOCATION_TYPES[node.name] = format_to_location_type(
                location_type_fragment=node
            )


def add_location_type(
    client: SymphonyClient,
    name: str,
    properties: List[PropertyDefinition],
    map_type: Optional[str] = None,
    map_zoom_level: int = 8,
    is_site: bool = False,
) -> LocationType:
    """This function creates new location type.

    :param name: Location type name
    :type name: str
    :param properties: List of property definitions
    :type properties: List[ :class:`~psym.common.data_class.PropertyDefinition` ]
    :param map_zoom_level: Map zoom level
    :type map_zoom_level: int

    :raises:
        FailedOperationException: Internal symphony error

    :return: LocationType object
    :rtype: :class:`~psym.common.data_class.LocationType`

    **Example**

    .. code-block:: python

        location_type = client.add_location_type(
            name="city",
            properties=[
                PropertyDefinition(
                    property_name="Contact",
                    property_kind=PropertyKind.string,
                    default_raw_value=None,
                    is_fixed=True
                )
            ],
            map_zoom_level=5,
        )
    """
    new_property_types = format_to_property_type_inputs(data=properties)
    result = AddLocationTypeMutation.execute(
        client,
        AddLocationTypeInput(
            name=name,
            mapZoomLevel=map_zoom_level,
            mapType=map_type if map_type else None,
            isSite=is_site,
            properties=new_property_types,
            surveyTemplateCategories=[],
        ),
    )

    location_type = format_to_location_type(location_type_fragment=result)
    LOCATION_TYPES[result.name] = location_type
    return location_type


def get_location_types(client: SymphonyClient) -> Iterator[LocationType]:
    """Get the iterator of location types

    :raises:
        FailedOperationException: Internal symphony error

    :return: LocationType Iterator
    :rtype: Iterator[ :class:`~psym.common.data_class.LocationType` ]

    **Example**

    .. code-block:: python

        location_types = client.get_location_types()
        for location_type in location_types:
            print(location_type.name)
    """
    result = LocationTypesQuery.execute(client)
    if result is None:
        return
    for edge in result.edges:
        node = edge.node
        if node is not None:
            yield format_to_location_type(location_type_fragment=node)


def get_location_type_by_id(client: SymphonyClient, id: str) -> LocationType:
    """This function gets existing LocationType by its ID.

    :param id: Location type ID
    :type id: str

    :raises:
        * FailedOperationException: Internal symphony error
        * :class:`~psym.exceptions.EntityNotFoundError`: Location type does not exist

    :return: Location type
    :rtype: :class:`~psym.common.data_class.LocationType`

    **Example**

    .. code-block:: python

        client.get_location_type_by_id(id="12345678")
    """
    result = LocationTypeDetailsQuery.execute(client, id=id)

    if result is None:
        raise EntityNotFoundError(entity=Entity.WorkOrderType, entity_id=id)

    return format_to_location_type(location_type_fragment=result)


def delete_locations_by_location_type(
    client: SymphonyClient, location_type: LocationType
) -> None:
    """Delete locatons by location type.

    :param location_type: LocationType object
    :type location_type: :class:`~psym.common.data_class.LocationType`

    :raises:
        `psym.exceptions.EntityNotFoundError`: `location_type` does not exist

    :rtype: None

    **Example**

    .. code-block:: python

        client.delete_locations_by_location_type(location_type=location_type)
    """
    location_type_with_locations = LocationTypeLocationsQuery.execute(
        client, id=location_type.id
    )
    if location_type_with_locations is None:
        raise EntityNotFoundError(
            entity=Entity.LocationType, entity_id=location_type.id
        )
    locations = location_type_with_locations.locations
    if locations is None:
        return
    for location in locations.edges:
        node = location.node
        if node:
            delete_location(
                client,
                Location(
                    id=node.id,
                    name=node.name,
                    latitude=node.latitude,
                    longitude=node.longitude,
                    external_id=node.externalId,
                    location_type_name=node.locationType.name,
                    properties=node.properties,
                ),
            )


def delete_location_type_with_locations(
    client: SymphonyClient, location_type: LocationType
) -> None:
    """Delete locaton type with existing locations.

    :param location_type: LocationType object
    :type location_type: :class:`~psym.common.data_class.LocationType`

    :raises:
        `psym.exceptions.EntityNotFoundError`: `location_type` does not exist

    :rtype: None

    **Example**

    .. code-block:: python

        client.delete_location_type_with_locations(location_type=location_type)
    """
    delete_locations_by_location_type(client, location_type)
    delete_location_type(client, location_type_id=location_type.id)


def delete_location_type(client: SymphonyClient, location_type_id: str) -> None:
    """This function deletes LocatoinType.

    :param location_type_id: Location type ID
    :type location_type_id: str

    :raises:
        * FailedOperationException: Internal symphony error
        * :class:`~psym.exceptions.EntityNotFoundError`: Location type does not exist

    **Example**

    .. code-block:: python

        client.delete_location_type(
            location_type_id="12345678"
        )
    """
    location_type = get_location_type_by_id(client=client, id=location_type_id)
    if location_type is None:
        raise EntityNotFoundError(
            entity=Entity.LocationType, entity_id=location_type_id
        )
    RemoveLocationTypeMutation.execute(client, id=location_type_id)
    del LOCATION_TYPES[location_type.name]
