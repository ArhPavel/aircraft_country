from typing import Any

from src.api import APIAdapter
from src.storage import JSONStorage


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем через консоль."""

    print("Добро пожаловать в систему отслеживания самолетов!")
    storage = JSONStorage()
    api_client = APIAdapter()

    while True:
        print("\n" + "=" * 50)
        print("Главное меню:")
        print("1. Найти самолеты над определенной страной (загрузка из API)")
        print("2. Вывести Топ-N самолетов по высоте полета (из локальной базы)")
        print("3. Найти самолеты по стране регистрации (из локальной базы)")
        print("0. Выход")
        print("=" * 50)

        choice = input("Выберите действие (введите номер): ").strip()

        if choice == "1":
            country = input("Введите название страны на английском (например, Canada): ").strip()
            print(f"\nЗапрашиваем координаты и скачиваем данные для {country}...")

            # Очищаем старые данные API-клиента перед новым запросом
            api_client.aeroplanes.clear()
            api_client.get_aeroplanes(country)

            if api_client.aeroplanes:
                print(f"Найдено самолетов: {len(api_client.aeroplanes)}.")

                # Дополнительная фича: спрашиваем, нужно ли сохранять
                save_choice = input("Сохранить эти данные в базу? (y/n): ").strip().lower()
                if save_choice == "y":
                    for aircraft in api_client.aeroplanes:
                        storage.add_aircraft(aircraft)
                    print("Данные успешно сохранены в data/aircrafts.json!")

        elif choice == "2":
            try:
                n = int(input("Введите количество самолетов (N): ").strip())
                saved_data: list[dict[str, Any]] = storage.get_aircrafts()

                if not saved_data:
                    print("Локальная база пуста. Сначала выполните загрузку (Пункт 1).")
                    continue

                # Сортируем список словарей по ключу altitude по убыванию (reverse=True)
                # Обязательно переводим в float для корректной сортировки mypy
                sorted_data = sorted(saved_data, key=lambda x: float(x.get("altitude", 0.0)), reverse=True)
                top_n = sorted_data[:n]

                print(f"\n--- ТОП-{n} САМОЛЕТОВ ПО ВЫСОТЕ ---")
                for i, plane in enumerate(top_n, start=1):
                    alt = plane.get("altitude")
                    callsign = plane.get("callsign")
                    country_reg = plane.get("country")
                    print(f"{i}. Позывной: {callsign} | Высота: {alt} м | Регистрация: {country_reg}")

            except ValueError:
                print("Ошибка: Пожалуйста, введите целое число.")

        elif choice == "3":
            reg_country = input("Введите страну регистрации для поиска (например, United States): ").strip()

            # Используем функционал нашего хранилища
            filtered_data = storage.get_aircrafts(country=reg_country)

            if filtered_data:
                print(f"\nНайдено {len(filtered_data)} самолетов, зарегистрированных в {reg_country}:")
                for plane in filtered_data[:10]:  # Выводим только первые 10, чтобы не засорять консоль
                    print(f" - Позывной: {plane.get('callsign')}, Скорость: {plane.get('velocity')} м/с")
                if len(filtered_data) > 10:
                    print(f" ... и еще {len(filtered_data) - 10} бортов.")
            else:
                print(f"В базе нет самолетов, зарегистрированных в стране '{reg_country}'.")

        elif choice == "0":
            print("Завершение работы программы. До свидания!")
            break

        else:
            print("Неверный ввод! Пожалуйста, выберите номер из меню.")


if __name__ == "__main__":
    # Очищаем консоль для красоты (работает на Windows)
    import os

    os.system("cls" if os.name == "nt" else "clear")

    user_interaction()
