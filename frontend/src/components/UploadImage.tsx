"use client"

export default function UploadImage({
  onSelect,
}: {
  onSelect: (file: File | null) => void
}) {
  return (
    <label className="cursor-pointer text-sm text-indigo-400 hover:underline">
      Upload Gambar
      <input
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => onSelect(e.target.files?.[0] || null)}
      />
    </label>
  )
}
