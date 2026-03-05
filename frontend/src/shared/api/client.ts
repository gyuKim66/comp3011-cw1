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

/**
 * DELETE helper
 * - 204 No Content 지원 (body가 없을 수 있음)
 */
export async function apiDelete(path: string): Promise<void> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "DELETE",
  });
  if (!res.ok) return handleError(res);

  // 204면 body 없음이 정상 → 그냥 종료
  if (res.status === 204) return;

  // 혹시 서버가 200/JSON을 주는 경우가 있어도 안전하게 처리
  await res.text().catch(() => "");
}