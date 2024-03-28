from pydantic import BaseModel
from datetime import datetime


class ClickInfoEventDTO(BaseModel):
    url: str
    click_time: datetime
    time_on_page: str
    event_time: datetime


class ClickInfoProduceEventDTO(ClickInfoEventDTO):
    user_id: str
    produce_timestamp: datetime


class ClickInfoResponse(BaseModel):
    message: str
