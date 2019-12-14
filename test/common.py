from unittest.mock import MagicMock

import open_weather_api.base


class FakeRequest:

    def ok(self):
        return True

    def json(self):
        return {}


open_weather_api.base.requests = MagicMock()
open_weather_api.base.requests.get.return_value = FakeRequest()

