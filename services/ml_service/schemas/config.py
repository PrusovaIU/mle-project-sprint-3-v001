from pydantic import BaseModel, Field
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Model(BaseModel):
    """
    Схема описания ML модели для конфига
    """
    path: Path = Field(description="Путь к файлу с весами модели catboost")


class Settings(BaseSettings):
    """
    Настройки приложения
    """
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
        env_file=".env"
    )
    model: Model
