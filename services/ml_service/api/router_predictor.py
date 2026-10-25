from fastapi import APIRouter
from ..schemas.response import ResponseData
from ..schemas.request import RequestData
from .deps.predict_handler import CatboostHandlerDep


router_predictor = APIRouter(
    prefix="/predictor",
    tags=["Предсказания"]
)


@router_predictor.post(
    "/run",
    summary="Получение предсказания",
    description="Получение прогнозирования стоимости объекта",
    response_model=ResponseData
)
def predict(data: RequestData, catboost_handler: CatboostHandlerDep):
    return catboost_handler.handle(data)

