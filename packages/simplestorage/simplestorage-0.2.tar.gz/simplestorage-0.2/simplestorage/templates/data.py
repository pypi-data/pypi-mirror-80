from typing import Optional
from pydantic import BaseModel


class DataUnit(BaseModel):
    uri: str = None
    name: str = None
    is_folder: bool = None
    content_bytes: Optional[bytes] = None
