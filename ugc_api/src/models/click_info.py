from datetime import datetime
from pydantic import BaseModel, Field, validator


class ClickInfoEventDTO(BaseModel):
    url: str
    click_time: datetime
    time_on_page: int
    event_timestamp: datetime

    @validator('event_timestamp', 'click_time')
    def event_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)


class ClickInfoProduceEventDTO(ClickInfoEventDTO):
    event_type: str = Field(default='click_info')
    user_id: str
    produce_timestamp: datetime

    @validator('produce_timestamp')
    def produce_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)
