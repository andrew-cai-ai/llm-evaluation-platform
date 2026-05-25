2026-05-21

Built first FastAPI evaluation endpoint.

Learned:

- Git SSH setup
- GitHub authentication
- FastAPI endpoint structure
- API docs generation
- Initial architecture for LLM evaluation systems



2026-05-22

Built initial LLM evaluation platform MVP.

Added:

- Model provider adapter layer
- OpenAI service skeleton
- Anthropic service skeleton
- Mock provider for local testing
- Error handling and failure response structure
- Latency tracking

Learned:

- Runtime dependency vs initialization dependency
- Python 3.9 compatibility issue (Optional vs | syntax)
- External provider failures should not break service startup
- Separation of API layer and service layer
- Provider abstraction improves future extensibility

2026-05-23

Added:

- Real OpenAI provider integration
- Retry and timeout handling
- Token usage tracking
- Latency tracking for real model calls

Learned:

- OpenAI quota/billing errors are external provider failures
- Token usage is a core metric for cost-aware LLM systems
- Latency and token usage should be captured together for evaluation infrastructure


2026-05-25

Added:

- Consistency evaluation endpoint
- Multi-run evaluation for the same prompt
- Aggregated token usage across runs
- Per-run latency tracking

Learned:

- Same prompt can produce different outputs
- Latency varies across repeated LLM calls
- Token usage can change even when the prompt is the same
- Consistency evaluation is a core part of LLM reliability
- 