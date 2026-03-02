// frontend/src/features/home/api.ts


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
  observed_at: string; // ISO datetime
  temp: number;
  feels_like: number | null;
  humidity: number | null;
  pressure: number | null;
  wind_speed: number | null;
  weather_main: string | null;
  weather_desc: string | null;
  weather_icon: string | null;
  rain_1h: number | null;
  snow_1h: number | null;
  source: string;
};

export type HomeItemDTO = {
  location: LocationDTO;
  latest: LatestObservationDTO | null;
};

export type HomeResponse = {
  generated_at: string;
  default: HomeItemDTO | null;
  list: HomeItemDTO[];
};

function getApiBaseUrl() {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!base) throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  return base.replace(/\/$/, "");
}

export async function getHome(): Promise<HomeResponse> {
  const url = `${getApiBaseUrl()}/home`;

  const res = await fetch(url, {
    // 서버 컴포넌트에서 호출될 수 있으니 캐시 끄는 게 안전
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`GET /home failed: ${res.status} ${res.statusText} ${text}`);
  }

  return (await res.json()) as HomeResponse;
}