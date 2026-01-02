"use client"

import { useState } from "react"
import UploadBox from "@/components/UploadBox"
import ResultCard from "@/components/ResultCard"
import { AnalysisResult } from "@/lib/types"

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)

  const analyze = async (fd: FormData) => {
    setLoading(true)
    setResult(null)

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
      <div className="max-w-xl mx-auto py-20 space-y-6">
        <h1 className="text-4xl font-bold text-center">
          TruthLens AI
        </h1>

        <UploadBox onAnalyze={analyze} loading={loading} />

        {result && <ResultCard result={result} />}
      </div>
    </main>
  )
}
