from fastapi import APIRouter, UploadFile, File
from app.graph.truthlens_graph import truthlens_graph
import base64

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()

    # 🔥 CONVERT BYTES → BASE64 STRING
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    state = truthlens_graph.invoke({
        "image_base64": image_base64
    })

    print("=== GRAPH STATE FINAL ===")
    for k, v in state.items():
        print(k, type(v))


    return {
        "verdict": state["result"]["verdict"],
        "confidence": state["result"]["confidence"],
        "explanation": state["result"]["explanation"],
        "sources": state.get("sources", []),  
    }
