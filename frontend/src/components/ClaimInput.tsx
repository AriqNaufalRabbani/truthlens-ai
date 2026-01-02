"use client"

export default function ClaimInput({
  value,
  onChange,
}: {
  value: string
  onChange: (v: string) => void
}) {
  return (
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Apakah benar informasi berikut..."
      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-4 text-sm text-white resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
      rows={4}
    />
  )
}
