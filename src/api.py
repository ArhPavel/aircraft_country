from abc import ABC, abstractmethod

from requests import get

from src.states import Aircraft


class BaseAPI(ABC):
    """Абстрактный класс для работы со сторонними API."""

    @abstractmethod
    def get_aeroplanes(self, country: str) -> None:
        """Абстрактный метод для получения данных о самолетах по названию страны."""
        pass


class APIAdapter(BaseAPI):
    """Класс для работы с платформами OpenStreetMap и OpenSky Network."""

    def __init__(self) -> None:
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes: list[Aircraft] = []

    def get_aeroplanes(self, country: str) -> None:
        headers_nominatim = {
            "User-Agent": "test-app/1.0",
        }
        params_nominatim: dict[str, str | int] = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        # 1. Запрос координат страны (OpenStreetMap)
        response_osm = get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)
        data_osm = response_osm.json()

        if not data_osm:
            print(f"Координаты для страны {country} не найдены.")
            return

        geo_coordinates = data_osm[0].get("boundingbox")

        params_opensky: dict[str, str] = {
            "lamin": str(geo_coordinates[0]),
            "lamax": str(geo_coordinates[1]),
            "lomin": str(geo_coordinates[2]),
            "lomax": str(geo_coordinates[3]),
        }

        # 2. Запрос списка самолетов в этих координатах (OpenSky Network)
        response_opensky = get(url=self.opensky_url, params=params_opensky)
        data_opensky = response_opensky.json()

        # 3. Распаковка и создание объектов
# 3. Распаковка и создание объектов
        states_list = data_opensky.get('states')

        if states_list:
            for state in states_list:
                try:
                    aircraft = Aircraft(
                        ICAO24=state[0],
                        Callsign=state[1].strip() if state[1] else "Unknown",
                        Country=state[2],
                        longitude=state[5],
                        latitude=state[6],
                        velocity=state[9],
                        altitude=state[7],
                    )
                    self.aeroplanes.append(aircraft)
                except ValueError as e:
                    # Если данные кривые (отрицательная высота/скорость), просто пропускаем этот самолет
                    print(f"Пропущен борт {state[0]}: {e}")
                    continue
        else:
            print(f"В заданном квадрате для страны {country} самолеты не найдены.")
