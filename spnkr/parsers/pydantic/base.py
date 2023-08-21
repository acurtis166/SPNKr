from pydantic import BaseModel


def _to_camel_case(string: str) -> str:
    """Convert a snake case string to camelCase."""
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


def _to_pascal_case(string: str) -> str:
    """Convert a snake case string to PascalCase."""
    return "".join(word.capitalize() for word in string.split("_"))


class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = _to_camel_case
        populate_by_name = True


class PascalCaseModel(BaseModel):
    class Config:
        alias_generator = _to_pascal_case
        populate_by_name = True
