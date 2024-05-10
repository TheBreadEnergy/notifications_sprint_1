from pydantic import BaseModel


class HealthcheckSchema(BaseModel):
    status: int
