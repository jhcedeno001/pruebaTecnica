from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Clase encargada de inicailizar variables de entorno.
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str
    debug: bool
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}"
            f"/{self.db_name}"
        )

    countries_api_base_url: str
    countries_api_timeout_seconds: float
    exchange_rate_primary_url: str
    exchange_rate_fallback_url: str
    exchange_rate_api_timeout_seconds: float
    geo_reference_dataset_url: str
    geo_reference_api_timeout_seconds: float
    conflicts_dataset_url: str
    conflicts_api_timeout_seconds: float
    http_breaker_fail_max: int
    http_breaker_reset_timeout_seconds: float
    http_rate_limit_per_second: float
    cors_origins: list[str]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
