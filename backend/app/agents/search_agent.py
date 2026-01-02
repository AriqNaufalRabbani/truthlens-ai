import os
import requests
import re

def build_search_query(image_text: str) -> str:
    """
    Ambil keyword penting dari hasil vision.
    """
    lines = image_text.splitlines()

    keywords = []
    for line in lines:
        line = line.strip()

        # ambil baris judul / berita
        if line.lower().startswith("judul") or line.lower().startswith("title"):
            keywords.append(line.split(":", 1)[-1].strip())

        if "KRL" in line or "Jabodetabek" in line:
            keywords.append(line)

    if not keywords:
        # fallback: ambil 1–2 kalimat pertama
        return " ".join(lines[:2])[:120]

    # gabungkan & batasi panjang
    query = " ".join(keywords)
    return re.sub(r"[^a-zA-Z0-9\s]", "", query)[:120]


SEARCHAPI_URL = "https://www.searchapi.io/api/v1/search"

def search_facts(image_text: str) -> dict:
    query = build_search_query(image_text)

    params = {
        "engine": "google",
        "q": query[:200],     # batasi panjang
        "num": 5,
        "api_key": os.getenv("SEARCHAPI_KEY")
    }
    # print(params)

    try:
        response = requests.get(SEARCHAPI_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        

        organic = data.get("organic_results", [])
        # print(organic)

        if not organic:
            return {
                "summary": "Tidak ditemukan hasil pencarian yang relevan.",
                "sources": []
            }
            
        print("=== SOURCES EXTRACTED ===")
        for r in organic[:5]:
            print(
                r.get("link"),
                r.get("display_link"),
                r.get("domain")
            )


        return {
            "summary": "\n".join(
                r.get("snippet", "") for r in organic[:5]
            ),
            "sources": [
                r.get("link")
                or r.get("display_link")
                or f"https://{r.get('domain')}"
                for r in organic[:5]
                if r.get("link") or r.get("display_link") or r.get("domain")
            ]
        }


    except Exception as e:
        print("SEARCHAPI ERROR:", e)
        return {
            "summary": "Pencarian gagal karena kendala jaringan.",
            "sources": []
        }
