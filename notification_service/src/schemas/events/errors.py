from pydantic import BaseModel


class QueueError(BaseModel):
    message: str = "QueueSendingError"
    description: list[str] = ["Ошибка при отправке в очередь"]
