export type Location = {
  id: number;
  name: string;
  country_code: string;
  lat: number;
  lon: number;
  is_featured: boolean;
  display_order: number;
  is_active: boolean;
};

export async function getLocations(): Promise<Location[]> {
  const res = await fetch("http://127.0.0.1:8000/locations");

  if (!res.ok) {
    throw new Error("Failed to fetch locations");
  }

  return res.json();
}