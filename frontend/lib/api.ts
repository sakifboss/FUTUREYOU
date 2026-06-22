import type { DecisionCreate, DecisionListItem, SimulationResponse, Source } from "@/types/futureyou";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function createDecision(payload: DecisionCreate) {
  return apiFetch<{ id: string; share_token: string; status: string }>("/api/decisions", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function simulateDecision(id: string) {
  return apiFetch<SimulationResponse>(`/api/decisions/${id}/simulate`, {
    method: "POST",
    body: "{}",
  });
}

export function regenerateDecision(id: string) {
  return apiFetch<SimulationResponse>(`/api/decisions/${id}/regenerate`, {
    method: "POST",
    body: "{}",
  });
}

export function getDecisions() {
  return apiFetch<DecisionListItem[]>("/api/decisions");
}

export function getSources() {
  return apiFetch<Source[]>("/api/sources");
}
