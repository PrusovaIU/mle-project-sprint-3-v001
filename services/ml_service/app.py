from fastapi import FastAPI
from .api.router_predictor import router_predictor
from .usecases.catboost_handler import CatboostHandler
from .core.config import settings


async def lifespan(_app: FastAPI):
    handler = CatboostHandler(pipeline_path=settings.pipeline.path)
    _app.state.catboost_handler = handler
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_predictor)
