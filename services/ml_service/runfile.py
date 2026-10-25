from fastapi import FastAPI
from .api.router_predictor import router_predictor


app = FastAPI()
app.include_router(router_predictor)
