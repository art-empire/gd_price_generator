from pathlib import Path

from pydantic import Field
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)
from typing import Any

from pydantic_settings.sources import PydanticBaseEnvSettingsSource

BASE_DIR = Path(__file__).parent.parent.parent


# class AliasOnlyEnvSettingsSource(PydanticBaseEnvSettingsSource):
#     """
#     Используем стандартный env-source, но отдаём значение
#     только если alias присутствует
#     """
#
#     def get_field_value(
#         self, field: FieldInfo, field_name: str
#     ) -> tuple[Any, str, bool]:
#         alias = field.alias
#
#         # если алиаса нет — пропускаем
#         if not alias:
#             return None, field_name, False
#
#         # вызываем стандартный env lookup
#         return super().get_field_value(field, field_name)


class PydanticBaseSettings(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            # env_settings,
            # dotenv_settings,
            # AliasOnlyEnvSettingsSource(settings_cls),
            YamlConfigSettingsSource(settings_cls),
            # file_secret_settings,
        )

    debug: bool = Field(
        default=True,
        alias="DEBUG",
    )
