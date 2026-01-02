from langgraph.graph import StateGraph
from app.agents.vision_agent import extract_text_from_image
from app.agents.search_agent import search_facts
from app.agents.reasoning_agent import verify_claim
import base64

class State(dict):
    image_base64: str | None
    text: str | None

    claim_text: str
    search_summary: str
    sources: list
    result: dict


graph = StateGraph(State)

# ======================
# VISION NODE (OPTIONAL)
# ======================
def vision_node(s: State):
    if not s.get("image_base64"):
        return {"claim_text": ""}

    image_bytes = base64.b64decode(s["image_base64"])
    image_text = extract_text_from_image(image_bytes)

    return {"claim_text": image_text}


# ======================
# MERGE TEXT + IMAGE
# ======================
def merge_text_node(s: State):
    parts = []

    if s.get("claim_text"):
        parts.append(s["claim_text"])

    if s.get("text"):
        parts.append(f"USER CLAIM:\n{s['text']}")

    return {"claim_text": "\n\n".join(parts).strip()}


# ======================
# SEARCH NODE
# ======================
def search_node(s: State):
    search_text = s["claim_text"]

    search_result = search_facts(search_text)

    # DuckDuckGo biasanya string → kita normalize
    if isinstance(search_result, str):
        return {
            "search_summary": search_result,
            "sources": []
        }

    return {
        "search_summary": search_result.get("summary", ""),
        "sources": search_result.get("sources", [])
    }


# ======================
# REASONING NODE
# ======================
def reasoning_node(s: State):
    result = verify_claim(
        s["claim_text"],
        s["search_summary"]
    )

    # 🔥 INJECT SOURCES KE RESULT
    result["sources"] = s.get("sources", [])

    return {
        "result": result
    }



# ======================
# GRAPH FLOW
# ======================
graph.add_node("vision", vision_node)
graph.add_node("merge", merge_text_node)
graph.add_node("search", search_node)
graph.add_node("reasoning", reasoning_node)

graph.set_entry_point("vision")

graph.add_edge("vision", "merge")
graph.add_edge("merge", "search")
graph.add_edge("search", "reasoning")

truthlens_graph = graph.compile()
