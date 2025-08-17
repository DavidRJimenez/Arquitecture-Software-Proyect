// lib/api/client.ts
import { getToken } from "./token";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

type Options = RequestInit & { skipAuth?: boolean };

export async function apiFetch<T = unknown>(endpoint: string, options: Options = {}): Promise<T> {
  const token = options.skipAuth ? null : getToken();

  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });

  // Intenta parsear JSON (éxito o error)
  let data: any = null;
  const text = await res.text();
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text || null;
  }

  if (!res.ok) {
    const detail = typeof data?.detail === "string"
      ? data.detail
      : data?.message ?? `Error ${res.status}`;
    throw new ApiError(res.status, detail);
  }

  return data as T;
}
