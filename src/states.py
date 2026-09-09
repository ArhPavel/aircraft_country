from abc import ABC, abstractmethod
from functools import total_ordering
from typing import Any


class PrintMixin:
    """Миксин, который печатает в консоль информацию о создании объекта."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self) -> str:
        attrs = ", ".join(f"{repr(v)}" for v in self.__dict__.values())
        return f"{self.__class__.__name__}({attrs})"


class AirplaneInformation(ABC):
    """Базовый абстрактный класс (шаблон)."""

    def __init__(
        self,
        ICAO24: str,
        Callsign: str,
        Country: str,
        longitude: float,
        latitude: float,
        velocity: float,
        altitude: float,
    ) -> None:
        self._ICAO24: str = ICAO24
        self.Callsign: str = Callsign
        self.Country: str = Country
        self.longitude: float = longitude
        self.latitude: float = latitude
        self.velocity: float = velocity
        self.altitude: float = altitude  # Добавили высоту

    @property
    @abstractmethod
    def ICAO24(self) -> str:
        pass


@total_ordering  # Этот декоратор автоматически допишет методы >, <=, >= на основе наших __eq__ и __lt__
class Aircraft(PrintMixin, AirplaneInformation):
    """Конкретный класс для создания объектов самолетов."""

    def __init__(
        self,
        ICAO24: str,
        Callsign: str,
        Country: str,
        longitude: float,
        latitude: float,
        velocity: float,
        altitude: float,
    ) -> None:

        # API иногда присылает None (null) вместо чисел. Заменяем их на 0.0
        velocity = float(velocity) if velocity is not None else 0.0
        altitude = float(altitude) if altitude is not None else 0.0

        # Скорость и высота не могут быть меньше нуля
        if velocity < 0:
            raise ValueError("Скорость самолета не может быть отрицательной!")
        if altitude < 0:
            raise ValueError("Высота полета не может быть отрицательной!")

        # Если валидация пройдена, инициализируем родительские классы
        super().__init__(ICAO24, Callsign, Country, longitude, latitude, velocity, altitude)

    @property
    def ICAO24(self) -> str:
        return self._ICAO24

    # === МЕТОДЫ СРАВНЕНИЯ ===
    def __eq__(self, other: object) -> bool:
        """Сравнивает два самолета на равенство по скорости и высоте."""
        if not isinstance(other, Aircraft):
            return NotImplemented
        return (self.velocity, self.altitude) == (other.velocity, other.altitude)

    def __lt__(self, other: object) -> bool:
        """Определяет, меньше ли этот самолет другого (сначала по скорости, затем по высоте)."""
        if not isinstance(other, Aircraft):
            return NotImplemented
        return (self.velocity, self.altitude) < (other.velocity, other.altitude)
