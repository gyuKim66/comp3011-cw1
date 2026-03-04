// frontend/src/features/observations/api.ts


import { apiGet, apiPost } from "@/shared/api/client";

export type LatestObservationDTO = {
  observed_at: string;
  temp: number;
  feels_like?: number | null;
  humidity?: number | null;
  pressure?: number | null;
  wind_speed?: number | null;
  weather_main?: string | null;
  weather_desc?: string | null;
  weather_icon?: string | null;
  rain_1h?: number | null;
  snow_1h?: number | null;
  source: string;
};

// ✅ 백엔드 스펙: POST /observations/fetch?location_id=123 (query)
export async function fetchObservation(locationId: number): Promise<any> {
  const id = Number(locationId);
  return apiPost(`/observations/fetch?location_id=${id}`, {});
}

// ✅ GET /observations/latest?location_id=123
export async function getLatestObservation(
  locationId: number
): Promise<LatestObservationDTO | null> {
  const id = Number(locationId);
  return apiGet<LatestObservationDTO | null>(`/observations/latest?location_id=${id}`);
}