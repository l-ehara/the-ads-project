from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    env: str = "dev"
    databricks_host: str | None = None
    databricks_token: str | None = None
    databricks_http_path: str | None = None
    model_config = SettingsConfigDict(env_file=(".env",), env_prefix="ADS_", extra="ignore")

settings = Settings()
