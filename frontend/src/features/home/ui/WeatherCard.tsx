// frontend/src/features/home/ui/WeatherCard.tsx

import type { HomeItemDTO } from "../api";

function fmtTime(iso: string) {
  const d = new Date(iso);
  return isNaN(d.getTime()) ? iso : d.toLocaleString();
}

export default function WeatherCard({
  item,
  variant = "normal",
}: {
  item: HomeItemDTO;
  variant?: "normal" | "default";
}) {
  const { location, latest } = item;

  return (
    <div
      style={{
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 16,
        background: variant === "default" ? "#f5f3ff" : "#fff",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
        <div>
          <div style={{ fontSize: 18, fontWeight: 800 }}>
            {location.name} <span style={{ color: "#6b7280" }}>({location.country_code})</span>
          </div>
          <div style={{ color: "#6b7280", fontSize: 13 }}>
            lat {location.lat}, lon {location.lon}
          </div>
        </div>

        {location.is_featured && (
          <div
            style={{
              fontSize: 12,
              padding: "4px 10px",
              borderRadius: 999,
              background: "#ede9fe",
              color: "#5b21b6",
              height: "fit-content",
              fontWeight: 700,
            }}
          >
            Featured
          </div>
        )}
      </div>

      <hr style={{ border: 0, borderTop: "1px solid #eee", margin: "12px 0" }} />

      {latest ? (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
          <div>
            <div style={{ fontSize: 12, color: "#6b7280" }}>Temperature</div>
            <div style={{ fontSize: 22, fontWeight: 900 }}>
              {latest.temp.toFixed(1)}°C
            </div>
            {latest.feels_like != null && (
              <div style={{ fontSize: 13, color: "#374151" }}>
                feels like {latest.feels_like.toFixed(1)}°C
              </div>
            )}
          </div>

          <div>
            <div style={{ fontSize: 12, color: "#6b7280" }}>Weather</div>
            <div style={{ fontSize: 14, fontWeight: 700 }}>
              {latest.weather_main ?? "—"}
            </div>
            <div style={{ fontSize: 13, color: "#374151" }}>
              {latest.weather_desc ?? ""}
            </div>
          </div>

          <div style={{ fontSize: 13, color: "#374151" }}>
            <b>Humidity:</b> {latest.humidity ?? "—"}
          </div>
          <div style={{ fontSize: 13, color: "#374151" }}>
            <b>Wind:</b> {latest.wind_speed ?? "—"}
          </div>

          <div style={{ gridColumn: "1 / -1", fontSize: 12, color: "#6b7280" }}>
            Observed at: {fmtTime(latest.observed_at)} · source: {latest.source}
          </div>
        </div>
      ) : (
        <div style={{ color: "#6b7280", fontSize: 13 }}>
          관측 데이터가 아직 없습니다. (latest = null)
        </div>
      )}
    </div>
  );
}