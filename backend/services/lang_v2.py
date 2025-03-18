from langgraph.graph import StateGraph
from typing import TypedDict, Dict, Any
from backend.services.chatbot_service import query_cognitive_search, vendor_normalization_str

# Define the state schema
class ChatbotState(TypedDict):
    context: Dict[str, Any]  # Flexible data field
    agent_role: str          # Tracks the next agent to run

# Initialize the graph
workflow = StateGraph(ChatbotState)

# Define simple agents
def user_query_agent(state: ChatbotState) -> ChatbotState:
    state["context"] = {"user_query": "Hello, how are you?"}
    state["agent_role"] = "data_retrieval"
    return state

def data_retrieval_agent(state: ChatbotState) -> ChatbotState:
    # state["context"] = ["Relevant doc 1", "Relevant doc 2"]
    # state["agent_role"] = "llm_agent"
    # return state
    query=state["context"] ["user_query"]
    # rel_docs=query_cognitive_search(query) # rel_docs is basically a string of content of all relevant docs
    rel_docs="string for some relevent docs"
    state["context"]={"rel_doc_str":rel_docs,"user_query":query}
    return state

def vendor_norm(state: ChatbotState) -> ChatbotState:
    rel_docs=state["context"]["rel_doc_str"]
    query=state["context"] ["user_query"]
    norm_text=vendor_normalization_str(rel_docs)
    state["context"]={"norm_text":norm_text,"user_query":query}
    return state

def query_struc(state: ChatbotState) -> ChatbotState:
    query=state["context"]["user_query"]
    norm=state["context"]["norm_text"]
    print("NORM========>",norm)
    print("query==========>",query)
    return state


def llm_agent(state: ChatbotState) -> ChatbotState:
    state["context"] = "I'm doing well, thanks for asking!"
    state["agent_role"] = "done"
    return state

# Add nodes (agents) to the workflow
workflow.add_node("user_query", user_query_agent)
workflow.add_node("data_retrieval", data_retrieval_agent)
workflow.add_node("llm_agent", llm_agent)
workflow.add_node("vendor_normalize",vendor_norm)
workflow.add_node("query_structure",query_struc)

# Define edges (flow between agents)
workflow.set_entry_point("user_query")
workflow.add_edge("user_query", "data_retrieval")
workflow.add_edge("data_retrieval","vendor_normalize")
workflow.add_edge("vendor_normalize","query_structure")
workflow.add_edge("query_structure","llm_agent")
# workflow.add_edge("data_retrieval", "llm_agent")


# Compile the graph
app = workflow.compile()

# Run the workflow
initial_state = {"context": {}, "agent_role": "user_query"}
for output in app.stream(initial_state):
    print(output)
