// frontend/src/features/home/ui/WeatherRow.tsx

import type { HomeItemDTO } from "../api";

function formatDateTime(iso: string) {
  const d = new Date(iso);
  if (isNaN(d.getTime())) return iso;
  return d.toLocaleString();
}

export default function WeatherRow({ item }: { item: HomeItemDTO }) {
  const { location, latest } = item;

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "220px 110px 1fr 220px",
        gap: 12,
        alignItems: "center",
        padding: "12px 10px",
        borderBottom: "1px solid #f1f5f9",
        fontSize: 14,
      }}
    >
      <div style={{ fontWeight: 800 }}>
        {location.name}{" "}
        <span style={{ color: "#6b7280", fontWeight: 600 }}>
          ({location.country_code})
        </span>

        {location.is_featured && (
          <span
            style={{
              marginLeft: 8,
              fontSize: 11,
              padding: "2px 8px",
              borderRadius: 999,
              background: "#ede9fe",
              color: "#5b21b6",
              fontWeight: 800,
            }}
          >
            Featured
          </span>
        )}
      </div>

      <div style={{ fontWeight: 900 }}>
        {latest ? `${latest.temp.toFixed(1)}°C` : "—"}
      </div>

      <div style={{ color: "#374151" }}>
        {latest ? (
          <>
            <span style={{ fontWeight: 700 }}>
              {latest.weather_main ?? "—"}
            </span>
            <span style={{ color: "#6b7280" }}>
              {latest.weather_desc ? ` · ${latest.weather_desc}` : ""}
            </span>
            <span style={{ color: "#6b7280" }}>
              {latest.humidity != null ? ` · humidity ${latest.humidity}` : ""}
              {latest.wind_speed != null ? ` · wind ${latest.wind_speed}` : ""}
            </span>
          </>
        ) : (
          <span style={{ color: "#9ca3af" }}>관측 데이터 없음</span>
        )}
      </div>

      <div style={{ fontSize: 12, color: "#6b7280", textAlign: "right" }}>
        {latest ? formatDateTime(latest.observed_at) : ""}
      </div>
    </div>
  );
}