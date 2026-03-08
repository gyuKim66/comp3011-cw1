// frontend/src/features/analytics/api.ts

import { apiGet } from "@/shared/api/client";

export type TemperatureStats = {
  location_id: number;
  avg_temp: number | null;
  min_temp: number | null;
  max_temp: number | null;
  count: number;
};

export type HumidityStats = {
  location_id: number;
  avg_humidity: number | null;
  min_humidity: number | null;
  max_humidity: number | null;
  count: number;
};

export type TemperatureTrendPoint = {
  date: string;
  avg_temp: number | null;
};

export type TemperatureTrend = {
  location_id: number;
  days: number;
  data: TemperatureTrendPoint[];
};

function buildQuery(params: Record<string, string | number | undefined>) {
  const search = new URLSearchParams();

  for (const [key, value] of Object.entries(params)) {
    if (value === undefined) continue;
    search.set(key, String(value));
  }

  const qs = search.toString();
  return qs ? `?${qs}` : "";
}

export async function getTemperatureStats(
  locationId: number,
  days?: number
): Promise<TemperatureStats> {
  const qs = buildQuery({
    location_id: locationId,
    days,
  });

  return apiGet<TemperatureStats>(`/analytics/temperature-stats${qs}`);
}

export async function getHumidityStats(
  locationId: number,
  days?: number
): Promise<HumidityStats> {
  const qs = buildQuery({
    location_id: locationId,
    days,
  });

  return apiGet<HumidityStats>(`/analytics/humidity-stats${qs}`);
}

export async function getTemperatureTrend(
  locationId: number,
  days: number
): Promise<TemperatureTrend> {
  const qs = buildQuery({
    location_id: locationId,
    days,
  });

  return apiGet<TemperatureTrend>(`/analytics/temperature-trend${qs}`);
}