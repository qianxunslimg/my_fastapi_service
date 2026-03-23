import { env } from "../env";
import type { BypAnalysisData, CommonResponse, ServiceHealthData } from "./types";

const API_PREFIX = "/api/v1";

type ApiErrorPayload = {
  message?: string;
  detail?: string;
};

function buildQuery(params: Record<string, string | number | undefined | null>) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") {
      return;
    }
    query.set(key, String(value));
  });
  const text = query.toString();
  return text ? `?${text}` : "";
}

function extractErrorMessage(response: Response, rawText: string) {
  const text = rawText.trim();
  if (text) {
    try {
      const payload = JSON.parse(text) as ApiErrorPayload;
      if (payload.message && payload.message.trim()) {
        return payload.message.trim();
      }
      if (payload.detail && payload.detail.trim()) {
        return payload.detail.trim();
      }
    } catch {
      return text;
    }
    return text;
  }
  return response.statusText || `请求失败（HTTP ${response.status}）`;
}

async function throwRequestError(response: Response): Promise<never> {
  const text = await response.text();
  throw new Error(extractErrorMessage(response, text));
}

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${env.apiBase}${path}`);
  if (!response.ok) {
    await throwRequestError(response);
  }
  return response.json() as Promise<T>;
}

export async function fetchServiceHealth() {
  return getJson<CommonResponse<ServiceHealthData>>(`${API_PREFIX}/system/health`);
}

export async function analyzeByp(url: string) {
  const query = buildQuery({ url });
  return getJson<CommonResponse<BypAnalysisData>>(`${API_PREFIX}/byp_analyze/${query}`);
}
