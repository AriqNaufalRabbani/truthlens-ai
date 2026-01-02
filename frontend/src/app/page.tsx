"use client"

import { useState } from "react"
import ClaimInput from "@/components/ClaimInput"
import UploadImage from "@/components/UploadImage"
import ResultReport from "@/components/ResultReport"
import { AnalysisResult } from "@/lib/types"

export default function Home() {
  const [text, setText] = useState("")
  const [image, setImage] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)

  const analyze = async () => {
    if (!text && !image) return alert("Isi teks atau upload gambar")

    const fd = new FormData()
    if (text) fd.append("text", text)
    if (image) fd.append("file", image)

    setLoading(true)
    const res = await fetch("/api/analyze", {
      method: "POST",
      body: fd,
    })

    const data = await res.json()
    setResult(data)
    setLoading(false)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 to-indigo-950 text-white">
      <div className="max-w-2xl mx-auto py-20 space-y-6">
        <h1 className="text-4xl font-bold text-center">TruthLens AI</h1>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <ClaimInput value={text} onChange={setText} />
          <div className="flex justify-between items-center">
            <UploadImage onSelect={setImage} />
            <button
              onClick={analyze}
              disabled={loading}
              className="bg-indigo-600 px-6 py-2 rounded"
            >
              {loading ? "Menganalisis..." : "Mulai Investigasi"}
            </button>
          </div>
        </div>

        {result && <ResultReport result={result} />}
      </div>
    </main>
  )
}
