from opentelemetry import trace
from opentelemetry.trace import get_tracer, SpanKind
import logging 
import random # <--- NEW REQUIRED IMPORT

# Setup a dedicated logger for troubleshooting tracing issues
trace_logger = logging.getLogger('tracing_debug')
# FIX: Use the constant logging.INFO to prevent application crash
trace_logger.setLevel(logging.INFO) 

# Initialize a tracer instance. This relies on the Dynatrace OneAgent
tracer = get_tracer(__name__)

# Log the initial state of the tracer provider
if trace.get_tracer_provider():
    trace_logger.info(f"Tracer Provider initialized successfully: {type(trace.get_tracer_provider())}")
else:
    trace_logger.error("Tracer Provider is NOT initialized. The Dynatrace OneAgent hook may have failed.")


# Helper to get the W3C Traceparent string for propagation
def get_current_traceparent():
    """
    Retrieves the current W3C Trace Context (traceparent) string 
    from the active OpenTelemetry span, or manually generates one 
    if the tracer is broken (all zeros).
    """
    span = trace.get_current_span()
    
    # Check 1: Is a valid trace active?
    if span and span.get_span_context().is_valid:
        ctx = span.get_span_context()
        trace_logger.info(f"Span is valid. Trace ID: {ctx.trace_id:032x}")
        # W3C format: 00-TraceID-SpanID-01 (version, trace-id, parent-id, flags)
        return f"00-{ctx.trace_id:032x}-{ctx.span_id:016x}-01"
    
    # Check 2: Did the tracer fail and return the dummy 'all zeros' context?
    elif span and span.get_span_context().trace_id == 0:
        # The OneAgent is not hooked. Manually create a new, valid W3C Trace ID.
        trace_id = hex(random.getrandbits(128))[2:].zfill(32)
        span_id = hex(random.getrandbits(64))[2:].zfill(16)
        
        new_traceparent = f"00-{trace_id}-{span_id}-01"
        trace_logger.warning(f"OneAgent failure detected (trace_id=0). Manually generating Trace ID: {new_traceparent}")
        return new_traceparent

    else:
        # Log the failure for diagnostics
        trace_logger.error("No valid span context found. Agent hook failed.")
            
    return None

def start_trace_span(span_name, kind=trace.SpanKind.SERVER):
    """
    Manually starts a new span.
    """
    # Log before starting the span
    trace_logger.info(f"Attempting to start span: {span_name}")
    
    # Start the span (returns the Context Manager)
    context_manager = tracer.start_as_current_span(span_name, kind=kind)
    
    # Log after starting 
    trace_logger.info(f"Context Manager for '{span_name}' started. Trace ID will be confirmed on get_current_traceparent.")
        
    # Return the Context Manager for the 'with ... as span:' block
    return context_manager