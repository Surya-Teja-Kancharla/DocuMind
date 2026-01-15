const API_BASE = import.meta.env.VITE_API_BASE;

/**
 * Upload a SINGLE document with progress
 */
export function uploadDocumentWithProgress(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();

    // 🔥 CRITICAL FIX
    formData.append("file", file);

    xhr.open("POST", `${API_BASE}/upload/`);

    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable && onProgress) {
        const percent = Math.round((e.loaded / e.total) * 100);
        onProgress(percent);
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        reject(
          new Error(
            xhr.responseText || `Upload failed (${xhr.status})`
          )
        );
      }
    };

    xhr.onerror = () => reject(new Error("Network error"));

    xhr.send(formData);
  });
}
