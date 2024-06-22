from dataclasses import dataclass


@dataclass(frozen=True)
class Recipe:
    name: str
    system: str
    executable: str
    args: list[str]
