"""Data deserialization methods."""
import base64
import datetime
import decimal
import uuid
from typing import Any, Callable, List, Mapping, NamedTuple, Optional, Union

from .deserialize_html import (HtmlAttributes, HtmlStripper, HtmlTags,
                               default_html_stripper)

Map = Callable[[Any], Any]
Record = Mapping[str, Any]


class MapDef(NamedTuple):
    extract: Map
    map: Map
    key: str


class Deserialize:
    """Contains deserialization methods. They take API data and turn it into domain data."""

    html_stripper: HtmlStripper = default_html_stripper

    @staticmethod
    def map_def(extract: Map, map: Map, key: str) -> MapDef:
        return MapDef(extract, map, key)

    @classmethod
    def register_html_stripper(cls, html_stripper: HtmlStripper) -> None:
        cls.html_stripper = html_stripper

    @classmethod
    def map(
        cls, map_defs: Union[List[MapDef], Mapping[str, Map]]
    ) -> Callable[[Any], Record]:
        """Retrurns a function that will map any input into a mapping."""

        def mapper(data: Any) -> Record:
            if isinstance(map_defs, list):
                return {d.key: d.map(d.extract(data)) for d in map_defs}
            return {k: v(data.get(k)) for (k, v) in map_defs.items()}

        return mapper

    @classmethod
    def list(cls, fn: Map) -> Callable[[List], List]:
        """Returns a function that will apply a map to all items in a list."""

        def mapper(data: List) -> List:
            try:
                return [fn(val) for val in data]
            except TypeError:
                return []

        return mapper

    @classmethod
    def int(cls, val: Any) -> Optional[int]:
        """Try to parse a value as an integer."""
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    @classmethod
    def float(cls, val: Any) -> Optional[float]:
        """Try to parse a value as a float."""
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @classmethod
    def date(cls, val: Any) -> Optional[datetime.date]:
        """Try to parse a value as an ISO date."""
        try:
            return datetime.date.fromisoformat(val)
        except (ValueError, TypeError):
            return None

    @classmethod
    def datetime(cls, val: Any) -> Optional[datetime.datetime]:
        """Try to parse a value as an ISO datetime."""
        try:
            return datetime.datetime.fromisoformat(val)
        except (ValueError, TypeError):
            return None

    @classmethod
    def uuid(cls, val: Any) -> Optional[uuid.UUID]:
        """Try to parse a value as an UUID."""
        try:
            return uuid.UUID(val)
        except (ValueError, TypeError):
            return None

    @classmethod
    def decimal(cls, val: Any) -> Optional[decimal.Decimal]:
        """Try to parse a decimal."""
        try:
            return decimal.Decimal(val)
        except (decimal.InvalidOperation, TypeError, ValueError):
            return None

    @classmethod
    def _text(
        cls, tags: HtmlTags, attributes: HtmlAttributes, val: Optional[str]
    ) -> Optional[str]:
        if val is None:
            return None

        val = str(val)
        if val is None:
            return None

        val = val.strip()
        if not val:
            return None

        val = cls.html_stripper(tags, attributes, val)

        return val

    @classmethod
    def text_with_html(
        cls, *, tags: HtmlTags = None, attributes: HtmlAttributes = None
    ) -> Callable[[Optional[str]], Optional[str]]:
        """Maps a value to a string."""

        def mapper(val: Optional[str]) -> Optional[str]:
            return cls._text(tags or [], attributes or {}, val)

        return mapper

    @classmethod
    def text(cls, val: Any) -> Optional[str]:
        return cls._text([], {}, val)

    @classmethod
    def base64(cls, val: Any) -> Optional[bytes]:
        """Try to parse base64 to bytes."""
        try:
            val = base64.b64decode(val, validate=True)
            if not val:
                return None
            return val
        except (TypeError, ValueError):
            return None
