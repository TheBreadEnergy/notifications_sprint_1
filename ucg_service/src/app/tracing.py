from flask_request_id_header.middleware import RequestID
from opentelemetry import trace
from opentelemetry.exporter.jaeger.proto.grpc import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from src.config import Config


def configure_tracing(app):
    collector_endpoint = f"{Config.JAEGER_HOST}:{Config.JAEGER_PORT}"
    RequestID(app)
    resource = Resource(attributes={"service.name": "ugc-service"})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(collector_endpoint=collector_endpoint, insecure=True)
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()
