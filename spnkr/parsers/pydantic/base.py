from pydantic import BaseModel


def to_pascal_case(string: str) -> str:
    """Convert a snake case string to PascalCase."""
    return "".join(word.capitalize() for word in string.split("_"))


class PascalCaseModel(BaseModel):
    class Config:
        alias_generator = to_pascal_case
        allow_population_by_field_name = True
