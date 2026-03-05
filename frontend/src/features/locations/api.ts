// frontend/src/features/locations/api.ts


import { apiGet, apiPatch, apiPost, apiDelete } from "@/shared/api/client";

export type Location = {
  id: number;
  name: string;
  country_code: string;
  lat: number;
  lon: number;
  is_featured: boolean;
  is_active: boolean;
  display_order?: number;

};

export async function getLocations(): Promise<Location[]> {
  return apiGet<Location[]>("/locations");
}

export type PatchLocationRequest = {
  is_featured?: boolean;
  is_active?: boolean;
  display_order?: number;
};

export async function patchLocation(
  locationId: number,
  body: PatchLocationRequest
): Promise<Location> {
  return apiPatch<Location, PatchLocationRequest>(`/locations/${locationId}`, body);
}

export async function deleteLocation(locationId: number): Promise<void> {
  await apiDelete(`/locations/${locationId}`);
}


export type LocationSearchItem = {
  name: string;
  country_code: string;
  lat: number;
  lon: number;
  state?: string | null;
};

export async function searchLocations(
  q: string,
  limit = 5
): Promise<LocationSearchItem[]> {
  const params = new URLSearchParams({ q, limit: String(limit) });
  return apiGet<LocationSearchItem[]>(`/locations/search?${params.toString()}`);
}

export type CreateLocationRequest = {
  name: string;
  country_code: string;
  lat: number;
  lon: number;
  is_active: boolean;
  is_featured: boolean;
  display_order?: number; // ✅ optional (서버 자동부여)
};

export async function createLocation(body: CreateLocationRequest): Promise<Location> {
  return apiPost<Location, CreateLocationRequest>("/locations", body);
}