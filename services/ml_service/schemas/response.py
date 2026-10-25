from pydantic import BaseModel, Field


class ResponseData(BaseModel):
    """
    Схема для результатов предсказания
    """
    user_id: int = Field(gt=0, description="ID пользователя")
    prediction: float = Field(
        gt=0,
        description="Прогнозируемая стоимость объекта"
    )
