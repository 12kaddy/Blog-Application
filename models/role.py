from enum import Enum, StrEnum
from typing import Dict, Any
from pydantic import GetJsonSchemaHandler


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

    @classmethod
    def __get_pydantic_json_schema__(cls,
                                    _core_schema_,
                                    handler:GetJsonSchemaHandler) -> Dict[str, Any]:
        return {
            "type":"string",
            "enum":[role.value for role in cls],
            "example":"user",
            "description":"User role with access levels"
        }

    @classmethod
    def admin_roles(cls)-> set['UserRole']:
        return {cls.ADMIN, cls.MODERATOR}