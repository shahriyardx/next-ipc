from dataclasses import dataclass


@dataclass
class Headers:
    Authorization: str


class IPCResponse:
    def __init__(self, data: dict):
        self._json = data
        self.endpoint = data["endpoint"]
        self.headers = Headers(**data["headers"])
        self.key_vals = ""

        for key, val in data["data"].items():
            setattr(self, key, val)
            self.key_vals += f"{key}={val} "

    def to_json(self):
        return self._json

    def __repr__(self):
        return f"<IPCResponse {self.key_vals.strip()}>"

    def __str__(self):
        return self.__repr__()
