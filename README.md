# Phoenix Instrumentation Minimal Example

This repo is a minimal example of instrumenting phoenix with langgraph and fetching the current or root span id from a node.

Dependencies are managed with `uv`. Simply run `uv sync` to install dependencies.

To run an example run `uv run <filename>`.
    * `uv run phoenix-instrumentation.py` will instrument using `phoenix.otel`
	* `uv run opentelemetry-instrumentation.py` will instrument using `opentelemetry-instrumentation`

Both examples will start a fastapi server using uvicorn with a single async endpoint, `/` which will simply return the root trace ID to you.

This trace ID can then be used against phoenix APIs for validation.

Tested and working against python 3.12.8
