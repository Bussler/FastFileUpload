import logging
import os
import sys
import tomllib

from pydantic import BaseModel


class LoggerConfig(BaseModel):
    level: int | None = None

    @staticmethod
    def from_string(input_string: str) -> "LoggerConfig":
        if input_string == "INFO":
            return LoggerConfig(level=logging.INFO)
        if input_string == "DEBUG":
            return LoggerConfig(level=logging.DEBUG)
        if input_string == "ERROR":
            return LoggerConfig(level=logging.ERROR)
        if input_string == "WARNING":
            return LoggerConfig(level=logging.WARNING)
        return LoggerConfig(level=logging.INFO)


def config_load() -> LoggerConfig:
    config_path = os.getenv("CONFIG_PATH", "./config.toml")
    if not os.path.exists(config_path):
        print(f"Config {config_path} does not exist, aborting parsing")
        return sys.exit(1)

    with open(config_path, "rb") as f:
        try:
            data = tomllib.load(f)
            logger: LoggerConfig = LoggerConfig.from_string(data["logging"]["level"])
        except Exception as e:
            print(f"Something went wrong in parsing the config file: {e}")
            return sys.exit(1)
    return logger


class ConfigController:
    """Controller to load and cache configs when they are needed. Implements the singleton pattern.

    Configs:
        Logger_CONFIG: LoggerConfig
    """

    _initialized: bool = False
    instance: "ConfigController"

    def __new__(cls) -> "ConfigController":
        if not cls._initialized:
            cls.instance = super(ConfigController, cls).__new__(cls)
            cls._initialized = True
        return cls.instance

    def __init__(self) -> None:
        self._logger_config: LoggerConfig | None = None

    def _init_configs(self) -> None:
        self._logger_config = config_load()

    @property
    def LOGGER_CONFIG(self) -> LoggerConfig:
        if self._logger_config is None:
            self._init_configs()
            assert self._logger_config is not None
        return self._logger_config


CONFIGS: ConfigController = ConfigController()
# use like CONFIGS.instance.LOGGER_CONFIG.level
