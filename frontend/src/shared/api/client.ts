// frontend/src/shared/api/client.ts


const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

if (!BASE_URL) {
  throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
}

async function handleError(res: Response): Promise<never> {
  const text = await res.text().catch(() => "");
  throw new Error(`API error: ${res.status} ${res.statusText} ${text}`);
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, { cache: "no-store" });
  if (!res.ok) return handleError(res);
  return (await res.json()) as T;
}

export async function apiPatch<T, B extends object>(path: string, body: B): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) return handleError(res);
  return (await res.json()) as T;
}

export async function apiPost<T, B extends object>(path: string, body: B): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) return handleError(res);
  return (await res.json()) as T;
}