// frontend/src/features/home/api.ts


import { apiGet } from "@/shared/api/client";

export type LocationDTO = {
  id: number;
  name: string;
  country_code: string;
  lat: number;
  lon: number;
  is_active: boolean;
  is_featured: boolean;
  display_order: number;
};

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

export type HomeItemDTO = {
  location: LocationDTO;
  latest: LatestObservationDTO | null;
};

export type HomeResponse = {
  generated_at: string;
  featured: HomeItemDTO[]; // ✅ 최대 2개
  list: HomeItemDTO[];
};

export async function getHome(): Promise<HomeResponse> {
  return apiGet<HomeResponse>("/home");
}