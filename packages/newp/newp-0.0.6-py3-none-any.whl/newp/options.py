import typing as t


Options = t.NamedTuple(
    "Options", [("type", str), ("name", str), ("directory", str)]
)
