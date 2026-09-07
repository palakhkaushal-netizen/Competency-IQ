export type SkillMetric = { name: string; score: number };

export type StudentAnalytics = {
  live_data: boolean;
  overall_readiness: number | null;
  assessed_skills: number;
  critical_gaps: number;
  skills: SkillMetric[];
  message: string | null;
};

const apiBase = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBase}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function getStudentAnalytics(): Promise<StudentAnalytics> {
  return request<StudentAnalytics>("/api/analytics/student");
}

export function getHealth(): Promise<{ api: string; database: string }> {
  return request<{ api: string; database: string }>("/health");
}
