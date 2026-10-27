"""
Скрипт для симуляции нагрузки
"""
import random

from locust import HttpUser, task, between


class PredictorUser(HttpUser):
    """Клиент для использования в locust"""

    @staticmethod
    def _random_payload() -> dict:
        """
        Генерация payload со случайными значениями.

        :return: Сформированный payload.
        """
        build_year = random.randint(1900, 2026)
        # оставлю доступным значение '5' для building_type_int, чтобы нагрузка
        # генерировала периодические ошибки, которые будут отображаться в
        # метриках:
        building_type_int = random.randint(0, 6)
        latitude = random.uniform(-90.0, 90.0)
        longitude = random.uniform(-180.0, 180.0)
        ceiling_height = random.uniform(1.0, 5.0)
        floors_total = random.randint(1, 50)
        floor = random.randint(1, floors_total)
        rooms = random.randint(1, 10)
        total_area = random.uniform(1.0, 500.0)

        return {
            "user_id": random.randint(1, 100_000),
            "models_features": {
                "build_year": build_year,
                "building_type_int": building_type_int,
                "latitude": latitude,
                "longitude": longitude,
                "ceiling_height": ceiling_height,
                "floors_total": floors_total,
                "floor": floor,
                "rooms": rooms,
                "total_area": total_area,
            },
        }

    wait_time = between(0.1, 1.0)

    @task
    def predict(self) -> None:
        payload = self._random_payload()
        with self.client.post(
            "/predictor/run",
            json=payload,
            headers={
                "accept": "*/*",
                "Content-Type": "application/json",
            },
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Unexpected status {response.status_code}: "
                    f"{response.text[:200]}"
                )
