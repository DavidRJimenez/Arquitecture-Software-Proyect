// Funciones para interactuar con el backend S3
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function uploadFile(file: File): Promise<string> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_URL}/s3/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Error al subir archivo");
  return await res.text();
}

export async function listFiles(): Promise<string[]> {
  const res = await fetch(`${API_URL}/s3/list`);
  if (!res.ok) throw new Error("Error al listar archivos");
  return await res.json();
}

export async function deleteFile(filename: string): Promise<boolean> {
  const res = await fetch(`${API_URL}/s3/delete/${encodeURIComponent(filename)}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Error al borrar archivo");
  return await res.json();
}
