from fastapi import FastAPI
from .api.router_predictor import router_predictor
from .usecases.catboost_handler import CatboostHandler
from .core.config import settings
from prometheus_fastapi_instrumentator import Instrumentator



async def lifespan(_app: FastAPI):
    handler = CatboostHandler(pipeline_path=settings.pipeline.path)
    _app.state.catboost_handler = handler
    yield {"catboost_handler": handler}


app = FastAPI(lifespan=lifespan)
app.include_router(router_predictor)

Instrumentator().instrument(app).expose(app, tags=["Метрики"])
