from pydantic import BaseModel, Field, model_validator
from typing import Self


class InputFeatures(BaseModel):
    """
    Входные признаки для предсказания
    """
    build_year: int = Field(
        ge=1900,
        description="Год постройки дома"
    )
    building_type_int: int = Field(
        ge=0,
        description="Тип дома"
    )
    latitude: float = Field(
        ge=-90,
        le=90,
        description="Широта расположения дома"
    )
    longitude: float = Field(
        ge=-180,
        le=180,
        description="Долгота расположения дома"
    )
    ceiling_height: float = Field(
        gt=0,
        description="Высота потолков"
    )
    floors_total: int = Field(
        gt=0,
        description="Количество этажей в доме"
    )
    floor: int = Field(
        gt=0,
        description="Этаж, на котором располагается объект"
    )
    rooms: int = Field(
        gt=0,
        description="Количество комнат"
    )
    total_area: float = Field(
        gt=0,
        description="Площадь объекта"
    )

    @model_validator(mode="after")
    def check_floor(self) -> Self:
        if self.floor > self.floors_total:
            raise ValueError(
                "Значение этажа объекта \"floor\" не может быть больше "
                "общего количества этажей в доме \"floors_total\"")
        return self


class RequestData(BaseModel):
    """
    Параметры входного запроса
    """
    user_id: int = Field(gt=0, description="ID пользователя")
    models_features: InputFeatures
