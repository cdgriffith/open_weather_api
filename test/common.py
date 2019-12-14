from unittest.mock import MagicMock
from dataclasses import dataclass
from typing import Dict

import open_weather_api.base


@dataclass()
class FakeRequest:

    text: str = "text area"
    ok: bool = True
    json_value: Dict = None
    status_code: int = 200

    def json(self):
        return self.json_value or {}


open_weather_api.base.requests = MagicMock()
open_weather_api.base.requests.get.return_value = FakeRequest()

