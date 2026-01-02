from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.graph.truthlens_graph import truthlens_graph
import base64

router = APIRouter()

@router.post("/analyze")
async def analyze(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
):
    # ❌ Tidak boleh kosong dua-duanya
    if not file and not text:
        raise HTTPException(
            status_code=400,
            detail="Either text or image must be provided"
        )

    image_base64 = None

    # ✅ Jika ada image → convert ke base64
    if file:
        image_bytes = await file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # 🔥 INVOKE LANGGRAPH
    state = truthlens_graph.invoke({
        "image_base64": image_base64,
        "text": text
    })

    # DEBUG (boleh dihapus nanti)
    print("=== GRAPH STATE FINAL ===")
    for k, v in state.items():
        print(k, type(v))

    result = state["result"]

    # ✅ RESPONSE CONSISTENT DENGAN FRONTEND
    return {
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "explanation": result["explanation"],
        "sources": result.get("sources", []),
    }
