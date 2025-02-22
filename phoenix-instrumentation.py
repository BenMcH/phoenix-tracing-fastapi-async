from typing import TypedDict
from langgraph.graph import StateGraph, END

from opentelemetry import trace as trace_api
from openinference.instrumentation.langchain import LangChainInstrumentor, get_ancestor_spans, get_current_span
from phoenix.otel import register

tracer_provider = register(endpoint="http://localhost:6006/v1/traces")
trace_api.set_tracer_provider(tracer_provider)

LangChainInstrumentor().instrument()

class GraphState(TypedDict):
    span: str

graph = StateGraph(GraphState)

def step(state):
    assert get_current_span() is not None
    root_span = get_ancestor_spans()[-1]
    return {"span": trace_api.format_span_id(root_span.get_span_context().span_id)}
    
graph.add_node("step", step)
graph.set_entry_point("step")

graph.add_edge("step", END)

graph = graph.compile()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    result = await graph.ainvoke({"span": "UNKNOWN - Phoenix Otel Register"})
    
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
