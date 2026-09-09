from typing import Any
from unittest.mock import MagicMock, patch


# Импортируем твой класс из нужного модуля
from src.api import APIAdapter


class TestAPIAdapter:

    # Важно: патчим функцию get именно там, куда она импортирована (в src.api),
    # а не саму библиотеку requests.
    @patch("src.api.get")
    def test_get_aeroplanes_success(self, mock_get: Any) -> None:
        # 1. Arrange (Подготовка)
        adapter = APIAdapter()

        # Настраиваем первый фейковый ответ (от OpenStreetMap)
        mock_response_osm = MagicMock()
        mock_response_osm.json.return_value = [
            {"boundingbox": ["41.6751053", "83.3362128", "-141.00187", "-52.6194085"]}
        ]

        # Настраиваем второй фейковый ответ (от OpenSky)
        mock_response_opensky = MagicMock()
        # Настраиваем второй фейковый ответ (от OpenSky) с полным списком индексов
        mock_response_opensky = MagicMock()
        mock_response_opensky.json.return_value = {
            "states": [
                [
                    "abc1234",  # 0: icao24
                    "CanadaAir",  # 1: callsign
                    "Canada",  # 2: country
                    12345678,  # 3: time_position
                    12345678,  # 4: last_contact
                    -79.61,  # 5: longitude
                    43.67,  # 6: latitude
                    1000.0,  # 7: baro_altitude
                    False,  # 8: on_ground
                    200.5,  # 9: velocity
                ]
            ]
        }

        # side_effect отдаст сначала ответ OSM, а при втором вызове - ответ OpenSky
        mock_get.side_effect = [mock_response_osm, mock_response_opensky]

        # 2. Act (Действие)
        adapter.get_aeroplanes("Canada")

        # 3. Assert (Проверки)
        # Проверяем, что функция get была вызвана ровно 2 раза
        assert mock_get.call_count == 2

        # Проверяем, что в списке создался ровно один объект Aircraft с правильными данными
        assert len(adapter.aeroplanes) == 1
        plane = adapter.aeroplanes[0]
        assert plane.ICAO24 == "abc1234"
        assert plane.Callsign == "CanadaAir"
        assert plane.Country == "Canada"
