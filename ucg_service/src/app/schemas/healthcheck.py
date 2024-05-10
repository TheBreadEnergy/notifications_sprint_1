from marshmallow import Schema, fields


class HealthcheckSchema(Schema):
    status = fields.Int(description="Ответ сервиса")


healthcheck_schema = HealthcheckSchema()
