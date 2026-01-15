const API_BASE = import.meta.env.VITE_API_BASE;

export function uploadDocumentWithProgress(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append("file", file);

    xhr.open("POST", `${API_BASE}/upload`);

    xhr.upload.onprogress = (event) => {
      console.log("UPLOAD PROGRESS EVENT", event.loaded, event.total);
      if (event.lengthComputable && onProgress) {
        const percent = Math.round((event.loaded / event.total) * 100);
        onProgress(percent);
      }
    };


    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        reject(new Error("Upload failed"));
      }
    };

    xhr.onerror = () => reject(new Error("Network error"));

    xhr.send(formData);
  });
}
