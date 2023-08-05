
from typing import Dict, Any


class Backend:

    def __init__(self, path: str):
        self.path = path

    def read(self) -> Dict[str, Any]:
        raise NotImplementedError

    def write(self, wr_dict: Dict[str, Any]) -> None:
        raise NotImplementedError

    @classmethod
    def _strip_quotes(cls, data: dict) -> dict:
        clean_dict = {}
        for key, value in data.items():
            if isinstance(value, dict):
                clean_dict[key] = cls._strip_quotes(value)
            else:
                clean_dict[key] = value.strip('"').strip("'")
        return clean_dict



