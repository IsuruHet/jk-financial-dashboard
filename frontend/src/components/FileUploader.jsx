import { useState } from "react";

export default function FileUploader({ onUploadComplete }) {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    setLoading(true);
    const res = await fetch(
      `${import.meta.env.VITE_API_BASE_URL}/api/extract`,
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await res.json();
    setLoading(false);
    onUploadComplete(data.data);

    // Refresh the page after upload is complete
    window.location.reload();
  };

  return (
    <div className="mb-4">
      <input
        type="file"
        accept="application/pdf"
        multiple
        onChange={(e) => setFiles([...e.target.files])}
      />
      <button
        onClick={handleUpload}
        disabled={files.length == 0 || loading}
        className="ml-2 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        {loading ? "Uploadng..." : "Upload PDFs"}
      </button>
      <div className="mb-4 flex justify-end">
        <a
          href={`${import.meta.env.VITE_API_BASE_URL}/api/download-all`}
          className="px-4 py-2 bg-emerald-600 text-white rounded hover:bg-emerald-700"
          download
        >
          Download CSV
        </a>
      </div>
    </div>
  );
}
