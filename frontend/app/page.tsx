"use client";

import { useEffect, useState } from "react";
import { getLocations, Location } from "@/features/locations/api";

export default function Home() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await getLocations();
        // featured 먼저 + display_order 정렬
        data.sort((a, b) =>
          a.is_featured === b.is_featured
            ? a.display_order - b.display_order
            : a.is_featured
            ? -1
            : 1
        );
        setLocations(data);
      } catch (e) {
        console.error("Failed to fetch locations", e);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return (
    <main style={{ padding: 32, fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: 26, fontWeight: 700 }}>
        🌍 Weather Dashboard
      </h1>

      {loading ? (
        <p style={{ marginTop: 20 }}>Loading locations...</p>
      ) : (
        <ul style={{ marginTop: 20 }}>
          {locations.map((loc) => (
            <li key={loc.id} style={{ marginBottom: 12 }}>
              <strong>{loc.name}</strong> ({loc.country_code})
              {loc.is_featured && (
                <span style={{ marginLeft: 10, color: "red" }}>
                  ⭐ Featured
                </span>
              )}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}