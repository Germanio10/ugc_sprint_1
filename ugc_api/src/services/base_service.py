from pydantic import BaseModel


class BaseService:
    def _get_key(self, data: BaseModel, exclude_fields: list[str] = []) -> bytes:
        return ':'.join([str(value) for _, value in data.model_dump(exclude=exclude_fields).items()]).encode()
    
    def _get_message(self, data: BaseModel) -> bytes:
        return data.model_dump_json().encode()