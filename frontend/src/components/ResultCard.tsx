import { AnalysisResult } from "@/lib/types"

export default function ResultCard({ result }: { result: AnalysisResult }) {
  return (
    <div className="bg-slate-900 p-6 rounded-xl space-y-4">
      {/* Verdict */}
      <h2 className="text-xl font-bold text-green-400">
        {result.verdict}
      </h2>

      {/* Confidence */}
      <div className="text-sm text-slate-300">
        Confidence: {result.confidence}%
      </div>

      {/* Explanation */}
      <p className="text-slate-200">
        {result.explanation}
      </p>

      {/* Sources */}
      {result.sources && result.sources.length > 0 && (
        <div className="pt-3 border-t border-slate-700">
          <h3 className="text-sm font-semibold text-slate-400 mb-2">
            Sumber:
          </h3>

          <ul className="list-disc list-inside space-y-1 text-sm">
            {result.sources.map((src, i) => (
              <li key={i}>
                <a
                  href={src}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:underline break-all"
                >
                  {src}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
