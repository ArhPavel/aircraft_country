import json
import os
from abc import ABC, abstractmethod
from typing import Any

# Импортируем класс Aircraft из твоего файла
from src.states import Aircraft


class BaseStorage(ABC):
    """Абстрактный класс для работы с хранилищем данных о самолетах."""

    @abstractmethod
    def add_aircraft(self, aircraft: Aircraft) -> None:
        """Добавляет информацию о самолете в хранилище."""
        pass

    @abstractmethod
    def get_aircrafts(self, **criteria: Any) -> list[dict[str, Any]]:
        """Получает данные о самолетах по указанным критериям."""
        pass

    @abstractmethod
    def delete_aircraft(self, **criteria: Any) -> None:
        """Удаляет информацию о самолетах по указанным критериям."""
        pass


class JSONStorage(BaseStorage):
    """Класс для сохранения информации о самолетах в JSON-файл."""

    def __init__(self, filepath: str = "data/aircrafts.json") -> None:
        self.filepath = filepath
        # Создаем файл и пустой список, если файла еще нет (чтобы избежать FileNotFoundError)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump([], file)

    def add_aircraft(self, aircraft: Aircraft) -> None:
        """Добавляет объект Aircraft в JSON-файл."""
        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Превращаем объект в словарь для сохранения
        aircraft_data = {
            "icao24": aircraft.ICAO24,
            "callsign": aircraft.Callsign,
            "country": aircraft.Country,
            "longitude": aircraft.longitude,
            "latitude": aircraft.latitude,
            "velocity": aircraft.velocity,
            "altitude": aircraft.altitude,
        }

        data.append(aircraft_data)

        with open(self.filepath, "w", encoding="utf-8") as file:
            # indent=4 делает файл читаемым, а ensure_ascii=False сохраняет правильную кодировку
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_aircrafts(self, **criteria: Any) -> list[dict[str, Any]]:  # <-- Добавили [str, Any]
        """
        Получает данные из файла.
        Критерии передаются через именованные аргументы: get_aircrafts(country="Canada")
        """
        with open(self.filepath, "r", encoding="utf-8") as file:
            # Явно говорим mypy, что именно мы прочитали из файла
            data: list[dict[str, Any]] = json.load(file)

        if not criteria:
            return data

        result = []
        for item in data:
            if all(item.get(k) == v for k, v in criteria.items()):
                result.append(item)
        return result

    def delete_aircraft(self, **criteria: Any) -> None:
        """Удаляет самолеты из файла по критериям. Заглушка для интеграции с БД."""
        if not criteria:
            return

        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Оставляем только те элементы, которые НЕ подходят под критерии удаления
        new_data = [item for item in data if not all(item.get(k) == v for k, v in criteria.items())]

        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(new_data, file, ensure_ascii=False, indent=4)
