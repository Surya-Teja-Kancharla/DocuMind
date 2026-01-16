const API_BASE = import.meta.env.VITE_API_BASE;

export function uploadDocumentWithProgress({
  file,
  userId,
  sessionId,
  onProgress,
}) {
  const xhr = new XMLHttpRequest();
  const formData = new FormData();

  formData.append("file", file);
  formData.append("user_id", userId);
  formData.append("session_id", sessionId);

  xhr.open("POST", `${API_BASE}/upload`);

  xhr.upload.onprogress = (e) => {
    if (e.lengthComputable && onProgress) {
      onProgress(Math.round((e.loaded / e.total) * 100));
    }
  };

  return new Promise((resolve, reject) => {
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        reject(xhr.responseText);
      }
    };

    xhr.onerror = () => reject("Upload failed");
    xhr.send(formData);
  });
}
