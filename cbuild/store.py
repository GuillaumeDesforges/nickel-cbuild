from typing import Protocol


class PStore(Protocol):
    def get_output_path(self, name: str) -> bytes:
        """
        Get the path to an output.
        """
        ...
