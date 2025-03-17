
from backend.services.chatbot_service import generate_embedding, query_cognitive_search, vendor_normalization, generate_llm_response
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, ValidationNode
from typing import Dict, TypedDict, Union, Sequence
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool
# from langchain_openai import ChatOpenAI

# from chatbot_service import generate_embedding, query_cognitive_search, vendor_normalization, generate_llm_response

# A simplified GraphState definition without ToolInvocation
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        keys: A dictionary mapping node names to their outputs.
    """
    keys: Dict[str, Union[str, int, float, bool, Sequence[BaseMessage]]]

# Simple node that generates an embedding
def generate_embedding_node(state: GraphState):
    """Generate embedding."""
    user_query = state['keys'].get("user_query")
    embedding = generate_embedding(user_query)
    if embedding:
        return {"keys": {"embedding": embedding}}
    return {"keys": {"error": "Embedding generation failed."}}

# Simple node that performs cognitive search
def cognitive_search_node(state: GraphState):
    """Perform cognitive search."""
    embedding = state['keys'].get("embedding")
    threshold = state['keys'].get("threshold", 0.7)
    documents = query_cognitive_search(embedding, threshold)
    return {"keys": {"documents": documents}}

# Simple node that normalizes vendor names
def vendor_normalization_node(state: GraphState):
    """Normalize vendor names."""
    documents = state['keys'].get("documents")
    normalized_documents = vendor_normalization(documents)
    return {"keys": {"documents": normalized_documents}}

# Simple node that generates an LLM response
def llm_response_node(state: GraphState):
    """Generate the final LLM response."""
    query = state['keys'].get("user_query")
    documents = state['keys'].get("documents")
    response = generate_llm_response(query, documents)
    return {"keys": {"response": response}}

# Build the LangGraph flow for the chatbot
def build_chatbot_graph():
    """Build and return the LangGraph for the chatbot flow"""
    graph = StateGraph(GraphState)
    graph.add_node("generate_embedding", generate_embedding_node)
    graph.add_node("cognitive_search", cognitive_search_node)
    graph.add_node("vendor_normalization", vendor_normalization_node)
    graph.add_node("llm_response", llm_response_node)

    # Set the flow sequence of execution
    graph.set_entry_point("generate_embedding")
    graph.add_edge("generate_embedding", "cognitive_search")
    graph.add_edge("cognitive_search", "vendor_normalization")
    graph.add_edge("vendor_normalization", "llm_response")
    graph.add_edge("llm_response", END)

    return graph.compile()

# Run the LangGraph flow for the chatbot
def chatbot_response(user_query, threshold=0.7):
    """Run the LangGraph flow for the chatbot"""
    graph = build_chatbot_graph()

    # Create input data for the flow
    input_data = {
        "keys": {
            "user_query": user_query,
            "threshold": threshold
        }
    }

    # Execute the flow
    result = graph.invoke(input_data)

    # Extract the final response
    response = result.get('response')
    if response:
        return {"answer": response}
    else:
        return {"error": "Something went wrong in the flow."}
