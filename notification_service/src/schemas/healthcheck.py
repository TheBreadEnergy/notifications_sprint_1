from pydantic import BaseModel


class HealthcheckSchema(BaseModel):
    code: int
