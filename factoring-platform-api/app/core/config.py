from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Factoring Platform API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")

    h2_driver: str = Field(default="org.h2.Driver", alias="H2_DRIVER")
    h2_jdbc_url: str = Field(
        default="jdbc:h2:tcp://localhost:9092/./factoring_platform",
        alias="H2_JDBC_URL",
    )
    h2_user: str = Field(default="sa", alias="H2_USER")
    h2_password: str = Field(default="", alias="H2_PASSWORD")
    h2_jar_path: str = Field(default="drivers/h2.jar", alias="H2_JAR_PATH")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()