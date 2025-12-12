# tracing_setup.py
# ---------------------------------------------------
# OpenTelemetry + Dynatrace OTLP exporter setup
# Provides:
#   - tracer = get_tracer(__name__)
#   - start_span(name)
#   - get_current_traceparent()
# ---------------------------------------------------

from opentelemetry import trace
from opentelemetry.trace import get_tracer
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import inject
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import logging

# ---------------------------------------
# CONFIGURE LOGGING
# ---------------------------------------
logger = logging.getLogger("otel_setup")
logger.setLevel(logging.INFO)

# ---------------------------------------
# 1. SET TRACER PROVIDER + DYNOTRACE OTLP EXPORTER
# ---------------------------------------
def init_tracer():
    try:
        provider = TracerProvider()

        # OTLP HTTP Exporter --> Dynatrace
        exporter = OTLPSpanExporter(
            endpoint="https://<YOUR-DYNATRACE-ENV>.live.dynatrace.com/api/v2/otlp",
            headers={"Authorization": "Api-Token <YOUR_API_TOKEN>"}
        )

        processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(processor)

        trace.set_tracer_provider(provider)
        logger.info("OpenTelemetry tracer initialized and exporting to Dynatrace OTLP.")

    except Exception as e:
        logger.error(f"Failed to initialize OpenTelemetry tracing: {e}")


# Initialize tracing immediately on import
init_tracer()

# Get tracer instance
tracer = get_tracer(__name__)


# ---------------------------------------
# 2. Start a span helper
# ---------------------------------------
def start_trace_span(span_name):
    """
    Starts a new OpenTelemetry span as the current active span.
    Usage:
        with start_trace_span("my-span"):
            ...
    """
    return tracer.start_as_current_span(span_name)


# ---------------------------------------
# 3. Generate W3C traceparent header for Redis/HTTP
# ---------------------------------------
def get_current_traceparent():
    """
    Returns the W3C traceparent header representing the current span.
    """
    propagator = TraceContextTextMapPropagator()
    carrier = {}
    propagator.inject(carrier)
    return carrier.get("traceparent", None)
