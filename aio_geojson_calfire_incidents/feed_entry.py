"""Generic GeoJSON feed entry."""
import calendar
import logging
from datetime import date, datetime
from time import strptime
from typing import Dict, Optional, Tuple

import pytz
from aio_geojson_client.feed_entry import FeedEntry
from geojson import Feature

from .consts import (
    ATTR_ID,
    ATTR_TITLE,
    ATTR_UPDATED,
    ATTR_CONTAINED,
    ATTR_BURNED,
    ATTR_STARTED
)

_LOGGER = logging.getLogger(__name__)


class CalfireFeedEntry(FeedEntry):
    """Generic GeoJSON feed entry."""

    def __init__(self, home_coordinates: Tuple[float, float], feature: Feature):
        """Initialise this service."""
        super().__init__(home_coordinates, feature)

    @property
    def title(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties(ATTR_TITLE)

    @property
    def external_id(self) -> str:
        """Return the external id of this entry."""
        # Find a suitable ID for the provided entry.
        external_id = self._search_in_feature(ATTR_ID)
        if not external_id:
            external_id = self._search_in_properties(ATTR_ID)
        if not external_id:
            external_id = self.title
        if not external_id:
            # Use geometry as ID as a fallback.
            external_id = hash(self.coordinates)
        return external_id

    @property
    def properties(self) -> Optional[Dict]:
        """Return all properties found for this entry."""
        if self._feature and self._feature.properties:
            return self._feature.properties
        return None

    @property
    def acresBurned(self) -> int:
        """Return the acres burned of this entry."""
        return self._search_in_properties(ATTR_BURNED)

    @property
    def contained(self) -> int:
        """Return the contaiment of this entry."""
        return self._search_in_properties(ATTR_CONTAINED)

    @property
    def started(self) -> datetime:
        """Return the time started of this entry."""
        return self._search_in_properties(ATTR_STARTED)

    @property
    def updated(self) -> datetime:
        """Return the last updated time of this entry."""
        return self._search_in_properties(ATTR_UPDATED)            