from langgraph.graph import StateGraph
from app.agents.vision_agent import extract_text_from_image
from app.agents.search_agent import search_facts
from app.agents.reasoning_agent import verify_claim
import base64

class State(dict):
    image_base64: str
    image_text: str
    search_summary: str
    sources: list
    result: dict

graph = StateGraph(State)

def vision_node(s: State):
    image_bytes = base64.b64decode(s["image_base64"])
    return {
        "image_text": extract_text_from_image(image_bytes)
    }

def search_node(s: State):
    search = search_facts(s["image_text"]) or {}
    
    print(search)
    return {
        "search_summary": search.get("summary", ""),
        "sources": search.get("sources", [])
    }


def reasoning_node(s: State):
    return {
        "result": verify_claim(
            s["image_text"],
            s["search_summary"]
        )
    }

graph.add_node("vision", vision_node)
graph.add_node("search", search_node)
graph.add_node("reasoning", reasoning_node)

graph.set_entry_point("vision")
graph.add_edge("vision", "search")
graph.add_edge("search", "reasoning")

truthlens_graph = graph.compile()
