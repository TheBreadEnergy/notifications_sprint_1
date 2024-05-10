from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from src.core.config import settings


def configure_tracing() -> None:
    collector_endpoint = settings.jaeger_endpoint_host
    resource = Resource(attributes={"service.name": "notification-service"})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=collector_endpoint,
                insecure=True,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )
