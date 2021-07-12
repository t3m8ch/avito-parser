from enum import Enum
from typing import Optional

from pydantic import BaseSettings
from urlpath import URL

# Edit this!
PARSE_MODE = "HTML"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

DEFAULT_DB_URL = "postgresql+asyncpg://localhost/avito_parser"


class UpdateMethod(str, Enum):
    WEBHOOKS = "webhooks"
    LONG_POLLING = "long_polling"


class LogLevel(str, Enum):
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"


class Config(BaseSettings):
    tg_token: str
    tg_admins_id: str
    tg_webhook_host: Optional[str]
    tg_webhook_path: str = "/bot"
    tg_skip_updates: bool = False

    webapp_host: str = "localhost"
    webapp_port: int = 3000

    log_level: LogLevel = LogLevel.INFO

    db_url: str = DEFAULT_DB_URL

    check_interval_seconds: int = 180

    redis_host: Optional[str]
    redis_port: int = 6379
    redis_db: Optional[int]
    redis_password: Optional[str]

    service_account_file_path: str = "gsheets_credentials.json"

    ssl_certificate_path: Optional[str]
    ssl_private_key_path: Optional[str]

    @property
    def tg_update_method(self) -> UpdateMethod:
        return UpdateMethod.LONG_POLLING if not self.tg_webhook_host else UpdateMethod.WEBHOOKS

    @property
    def tg_webhook_url(self) -> str:
        return str(URL(self.tg_webhook_host, self.tg_webhook_path))

    @property
    def tg_parse_mode(self) -> str:
        # PARSE_MODE must be specified in the code, because the way
        # the message is parsed directly affects the code
        return PARSE_MODE

    @property
    def log_format(self):
        # LOG_FORMAT must be specified in the code,
        # because The format depends on the logging library used
        return LOG_FORMAT

    @property
    def is_redis(self):
        return self.redis_host is not None

    @property
    def ssl_is_set(self):
        return all([
            self.ssl_certificate_path is not None,
            self.ssl_private_key_path is not None,
        ])


config = Config(
    _env_file=".env",
    _env_file_encoding="utf-8"
)
