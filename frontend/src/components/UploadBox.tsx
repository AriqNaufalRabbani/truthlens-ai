"use client"

import { useState } from "react"

export default function UploadBox({
  onAnalyze,
  loading,
}: {
  onAnalyze: (fd: FormData) => void
  loading: boolean
}) {
  const [file, setFile] = useState<File | null>(null)

  return (
    <div className="bg-slate-800 p-6 rounded-xl space-y-4">
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="text-sm"
      />

      <button
        disabled={!file || loading}
        onClick={() => {
          const fd = new FormData()
          if (file) fd.append("file", file)
          onAnalyze(fd)
        }}
        className="w-full bg-indigo-600 hover:bg-indigo-700 py-2 rounded text-white"
      >
        {loading ? "Menganalisis..." : "Mulai Investigasi"}
      </button>
    </div>
  )
}
