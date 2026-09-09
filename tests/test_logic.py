from typing import Any

import pytest

from src.states import Aircraft
from src.storage import JSONStorage


# === ФИКСТУРЫ ===
@pytest.fixture
def slow_low_plane() -> Aircraft:
    """Фикстура: медленный самолет на низкой высоте."""
    return Aircraft("111", "SLOW1", "Russia", 37.0, 55.0, 100.0, 1000.0)


@pytest.fixture
def fast_high_plane() -> Aircraft:
    """Фикстура: быстрый самолет на большой высоте."""
    return Aircraft("222", "FAST2", "Canada", -79.0, 43.0, 250.0, 10000.0)


# === ТЕСТЫ ДЛЯ КЛАССА AIRCRAFT (Модели и ООП) ===
def test_aircraft_initialization(slow_low_plane: Aircraft) -> None:
    """Тест: проверяем инкапсуляцию и правильное сохранение атрибутов."""
    assert slow_low_plane.ICAO24 == "111"
    assert slow_low_plane.Callsign == "SLOW1"
    assert slow_low_plane.velocity == 100.0


def test_aircraft_validation() -> None:
    """Тест: проверяем, что класс не позволяет создать самолет с отрицательной высотой или скоростью."""
    with pytest.raises(ValueError, match="Скорость самолета не может быть отрицательной!"):
        Aircraft("333", "ERR", "USA", 0.0, 0.0, -50.0, 1000.0)

    with pytest.raises(ValueError, match="Высота полета не может быть отрицательной!"):
        Aircraft("333", "ERR", "USA", 0.0, 0.0, 100.0, -100.0)


def test_aircraft_comparison(slow_low_plane: Aircraft, fast_high_plane: Aircraft) -> None:
    """Тест: проверяем методы сравнения (__eq__, __lt__)."""
    assert slow_low_plane < fast_high_plane
    assert slow_low_plane != fast_high_plane


# === ТЕСТЫ ДЛЯ КЛАССА JSONStorage (Хранилище) ===
def test_json_storage_add_and_get(tmp_path: Any, slow_low_plane: Aircraft) -> None:
    """
    Тест: проверяем запись и чтение из JSON.
    Используем tmp_path, чтобы тест создал временный файл, который удалится сам.
    """
    # Создаем путь к временному файлу
    test_file = tmp_path / "test_aircrafts.json"

    # Инициализируем хранилище с этим временным путем
    storage = JSONStorage(filepath=str(test_file))

    # Добавляем самолет
    storage.add_aircraft(slow_low_plane)

    # Читаем данные обратно
    saved_data = storage.get_aircrafts()

    # Проверяем, что сохранилась ровно 1 запись и данные совпадают
    assert len(saved_data) == 1
    assert saved_data[0]["icao24"] == "111"
    assert saved_data[0]["country"] == "Russia"


def test_json_storage_filtering(tmp_path: Any, slow_low_plane: Aircraft, fast_high_plane: Aircraft) -> None:
    """Тест: проверяем поиск по критериям."""
    test_file = tmp_path / "test_aircrafts.json"
    storage = JSONStorage(filepath=str(test_file))

    storage.add_aircraft(slow_low_plane)
    storage.add_aircraft(fast_high_plane)

    # Ищем канадские самолеты
    canada_planes = storage.get_aircrafts(country="Canada")

    assert len(canada_planes) == 1
    assert canada_planes[0]["callsign"] == "FAST2"
