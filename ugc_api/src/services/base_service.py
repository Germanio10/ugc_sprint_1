from pydantic import BaseModel


class BaseService:

    def _get_key(self, event_name: str, data: BaseModel, include_fields: list[str] = []) -> bytes:
        fields = ':'.join([str(value) for _, value in data.model_dump(include=include_fields).items()])
        return f'{event_name}:{fields}'.encode()

    def _get_message(self, data: BaseModel) -> bytes:
        return data.model_dump_json().encode()
