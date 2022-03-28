from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseConfig, BaseModel


def convert_datetime(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')


class OrangeBaseModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {datetime: convert_datetime}

    pk: Optional[int] = None
