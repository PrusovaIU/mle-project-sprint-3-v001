import logging

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from enum import Enum
from fastapi import HTTPException, status
from .schemas.request import InputFeatures, RequestData
from .schemas.response import ResponseData


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CatboostHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    DISTANCE_TO_CENTER = "distance_to_center"

    PARAM_TYPES = {
        "user_id": str,
        "model_params": dict
    }

    def __init__(self, model_path: str):
        """
        :param model_path: Путь к файлу с весами моделей.
        """
        self._model_path = model_path
        self._model = self._load_credit_model(model_path=self._model_path)

    @staticmethod
    def _load_credit_model(model_path: str) -> CatBoostRegressor | None:
        """
        Загрузка обученной модели.

        :param model_path: Путь до модели.

        :return: Обученная модель.
        """
        try:
            model = CatBoostRegressor()
            model.load_model(model_path)
            logger.info(f"Модель успешно загружена из {model_path}")
        except Exception:
            logger.exception(f"Не удалось загрузить модель из {model_path}")
            raise
        return model

    @staticmethod
    def _calc_distance(lat1, lon1, lat2=55.45, lon2=37.37) -> float:
        """
        Расчет от центра в км по формуле Haversine.

        :param lat1: Широта объекта.
        :param lon1: Долгота объекта.
        :param lat2: Широта центра.
        :param lon2: Долгота центра.

        :return: Расстояние от объекта до центра.
        """
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(
            dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        return R * c

    def _price_predict(self, model_params: InputFeatures) -> float:
        """
        Предсказание стоимости объекта.

        :param model_params: Параметры для модели.

        :return: Предсказание модели.
        """
        if self._model is None:
            raise RuntimeError("Модель не загружена")

        params = model_params.model_dump()

        # генерация признака distance_to_center
        params["distance_to_center"] = self._calc_distance(
            float(params["latitude"]),
            float(params["longitude"])
        )

        X = pd.DataFrame(params)

        prediction = self._model.predict(X)
        return float(np.asarray(prediction).ravel()[0])

    def handle(self, params: RequestData) -> ResponseData:
        """Функция для обработки запросов API.

        :param params: Параметры запроса.

        :return: Ответ с предсказанием.
        """
        try:
            y_pred = self._price_predict(params.models_features)
            response = ResponseData(
                user_id=params.user_id,
                prediction=y_pred
            )
        except Exception as err:
            logger.exception("Ошибка при предсказании")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )
        return response
