from uvicorn import run
from services.ml_service.app import app


if __name__ == '__main__':
    run(
        app,
        host="127.0.0.1",
        port=8080
    )
