import ConfidenceBar from "./ConfidenceBar"
import { AnalysisResult } from "@/lib/types"

export default function ResultReport({ result }: { result: AnalysisResult }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Laporan Investigasi</h3>
        <span className="text-xs text-slate-400">TruthLens AI</span>
      </div>

      <div
        className={`py-2 rounded-lg text-center font-bold ${
          result.verdict === "BENAR"
            ? "bg-green-600"
            : result.verdict === "SALAH"
            ? "bg-red-600"
            : "bg-yellow-500"
        }`}
      >
        {result.verdict}
      </div>

      <ConfidenceBar value={result.confidence} />

      <div className="bg-slate-800 p-4 rounded text-sm text-slate-200">
        {result.explanation}
      </div>

      <div>
        <h4 className="text-sm font-semibold mb-2">Sumber Terverifikasi</h4>
        <ul className="list-disc list-inside text-sm text-blue-400 space-y-1">
          {result.sources.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>

      <div className="flex gap-3 pt-2">
        <button className="bg-green-600 px-4 py-2 rounded text-sm">
          Download / Share
        </button>
        <button className="bg-slate-700 px-4 py-2 rounded text-sm">
          Analisis Baru
        </button>
      </div>
    </div>
  )
}
