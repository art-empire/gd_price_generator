from functools import lru_cache

from pydantic import Field, ConfigDict

from settings.base import PydanticBaseSettings, BASE_DIR


class UserGroupConfig(PydanticBaseSettings):
    group_name: str
    row: str
    group_id:int



class Config(PydanticBaseSettings):

    model_config = ConfigDict(
        yaml_file= BASE_DIR / 'config' / 'app_config.yaml'
    )
    user_groups: list[UserGroupConfig] = Field(default_factory=list)


@lru_cache(1)
def get_config() -> Config:

    return Config()