"""Contains an extension to ntier.Deserialize specialized for working with aiohttp requests."""
from typing import Any, Callable, List, Mapping, NamedTuple, Optional

from multidict import MultiDict
from ntier.deserialize import Deserialize as DeserializeBase
from ntier.deserialize import Map, MapDef

OpStr = Optional[str]


class RequestData(NamedTuple):
    query: MultiDict
    match_info: Mapping[str, str]
    body: Any


class Deserialize(DeserializeBase):
    """An extension to ntier.Deserialize specialized for working with aiohttp Requests."""

    @classmethod
    def query_item(
        cls, key: str, map: Map, output_key: OpStr = None, fallback: OpStr = None
    ) -> MapDef:
        """Get a query string item."""

        def extract(data: RequestData) -> OpStr:
            return data.query.get(key, fallback)

        return cls.map_def(extract, map, output_key or key)

    @classmethod
    def query_list(cls, key: str, map_item: Map, output_key: OpStr = None) -> MapDef:
        """Get a list of query string items."""

        def extract(data: RequestData) -> List[str]:
            return data.query.getall(key, [])

        return cls.map_def(extract, cls.list(map_item), output_key or key)

    @classmethod
    def match_info(
        cls, key: str, map: Map, output_key: OpStr = None, fallback: OpStr = None
    ) -> MapDef:
        """Get a url match."""

        def extract(data: RequestData) -> OpStr:
            return data.match_info.get(key, fallback)

        return cls.map_def(extract, map, output_key or key)

    @classmethod
    def body(cls, map: Map, output_key: str) -> MapDef:
        """Map the entire body of a request."""

        def extract(data: RequestData) -> Any:
            return data.body

        return cls.map_def(extract, map, output_key)

    @classmethod
    def body_prop(
        cls, key: str, map: Map, output_key: OpStr = None, fallback: Any = None
    ) -> MapDef:
        """Map a prop from the body of a request. Assumes the body deserialized into a Mapping"""

        def extract(data: RequestData) -> Any:
            return data.body.get(key, fallback)

        return cls.map_def(extract, map, output_key or key)

    @classmethod
    def body_path(
        cls, path: List[str], map: Map, output_key: str, fallback: Any = None
    ) -> MapDef:
        """Map a value from a path in the body of a request. Assumes the body deserialized into a
        Mapping and that ever level of the path is similarly a Mapping.
        """

        def extract(data: RequestData) -> Any:
            parts = list(reversed(path))
            value = data.body
            while parts:
                key = parts.pop()
                if key in value:
                    value = value[key]
                else:
                    return fallback
            return value

        return cls.map_def(extract, map, output_key)
