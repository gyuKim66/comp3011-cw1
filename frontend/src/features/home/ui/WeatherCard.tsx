// frontend/src/features/home/ui/WeatherCard.tsx



"use client";

import type { HomeItemDTO } from "../api";

function fmtTime(iso: string) {
  const d = new Date(iso);
  if (isNaN(d.getTime())) return iso;

  return d.toLocaleString("en-GB", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });
}

type Props = {
  item: HomeItemDTO;
  variant: "default" | "secondary";
  onDelete?: () => void; // ✅ 추가
};

export default function WeatherCard({ item, variant, onDelete }: Props) {
  // ✅ 기존 날씨 표시 로직이 있다면 아래 “표시 부분”은 그대로 유지하세요.
  const locationName = (item as any)?.location?.name ?? "Unknown";
  // ✅ 핵심 수정: observation이 아니라 latest를 읽는다
  const temp = (item as any)?.latest?.temp;
  const weather = (item as any)?.latest?.weather_desc ?? (item as any)?.latest?.weather_main ?? "—";
  const observedAt = (item as any)?.latest?.observed_at ?? "";

  return (
    <div
      style={{
        borderRadius: 16,
        padding: 18,
        background: "#ffffff",
        boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
        border: "1px solid #e5e7eb",
      }}
    >
      {/* ✅ 변경된 부분: 삭제 버튼 추가 */}
      <div
        style={{
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "space-between",
          gap: 12,
          marginBottom: 10,
        }}
      >
        <div style={{ minWidth: 0 }}>
          <div style={{ fontSize: 18, fontWeight: 900, color: "#111827" }}>
            {locationName}
          </div>
          <div style={{ marginTop: 4, fontSize: 12, fontWeight: 800, color: "#6b7280" }}>
            {variant === "default" ? "Featured" : "Secondary"}
          </div>
        </div>

        <button
          type="button"
          onClick={onDelete}
          disabled={!onDelete}
          style={{
            border: "1px solid #e5e7eb",
            background: "#fff",
            borderRadius: 10,
            padding: "6px 10px",
            fontSize: 12,
            fontWeight: 900,
            cursor: onDelete ? "pointer" : "not-allowed",
            opacity: onDelete ? 1 : 0.5,
            whiteSpace: "nowrap",
          }}
          aria-label="Remove this card"
          title="Remove"
        >
          삭제
        </button>
      </div>

      {/* ✅ 기존 날씨 정보 표시 영역 (유지) */}
      <div style={{ display: "grid", gap: 8 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
          <div style={{ fontSize: 40, fontWeight: 950, lineHeight: 1 }}>
            {temp === null || temp === undefined ? "--°" : `${Math.round(Number(temp))}°`}
          </div>
          <div style={{ fontSize: 14, color: "#374151", fontWeight: 800 }}>
            {String(weather)}
          </div>
        </div>

        {observedAt ? (
          <div style={{ fontSize: 12, color: "#6b7280", fontWeight: 700 }}>
            Observed at: {fmtTime(String(observedAt))}
          </div>
        ) : (
          <div style={{ fontSize: 12, color: "#9ca3af", fontWeight: 700 }}>
            Observed at: —
          </div>
        )}
      </div>
    </div>
  );
}