import { useState } from "react";
import { uploadDocumentWithProgress } from "../api/upload";

const DocumentUpload = ({ onUploadComplete }) => {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  const handleChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setProgress(0);
    setError(null);

    const startTime = Date.now();

    try {
      await uploadDocumentWithProgress(file, setProgress);

      // UX guard (minimum visible time)
      const elapsed = Date.now() - startTime;
      if (elapsed < 800) {
        await new Promise(r => setTimeout(r, 800 - elapsed));
      }

      onUploadComplete();
    } catch {
      setError("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="border-b bg-white/5 px-6 py-3">
      <div className="flex justify-between items-center">
        <span className="text-sm text-slate-300">
          {uploading
            ? `Uploading… ${progress}%`
            : "Upload a document to begin"}
        </span>

        <label className="cursor-pointer">
          <input
            type="file"
            hidden
            onChange={handleChange}
            disabled={uploading}
          />
          <span className={`px-4 py-1.5 rounded ${
            uploading ? "bg-slate-600" : "bg-slate-900 text-white"
          }`}>
            {uploading ? "Uploading…" : "Upload Document"}
          </span>
        </label>
      </div>

      {uploading && (
        <div className="mt-3 w-full bg-slate-700 rounded h-2">
          <div
            className="h-full bg-blue-600 transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {error && <div className="mt-2 text-red-500">{error}</div>}
    </div>
  );
};

export default DocumentUpload;
