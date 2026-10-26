from ...usecases.catboost_handler import CatboostHandler
from fastapi import Depends, Request
from typing import Annotated


def catboost_handler(request: Request) -> CatboostHandler:
    """
    :return: Класс `CatboostHandler` с загруженной моделью.
    """
    return request.state.catboost_handler


CatboostHandlerDep = Annotated[
    CatboostHandler,
    Depends(catboost_handler)
]
