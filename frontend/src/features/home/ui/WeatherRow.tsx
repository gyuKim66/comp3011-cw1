// frontend/src/features/home/ui/WeatherRow.tsx


"use client";

type Props = {
  item: any;
  onPromote: () => void;
};

function fmtTimeStable(iso: string) {
  const d = new Date(iso);
  if (isNaN(d.getTime())) return iso;
  // ✅ locale mismatch(수화 오류) 방지: 고정 포맷
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  const hh = String(d.getHours()).padStart(2, "0");
  const mi = String(d.getMinutes()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd} ${hh}:${mi}`;
}

export default function WeatherRow({ item, onPromote }: Props) {
  // ✅ 핵심: Home API / optimistic 모두 "latest" 구조를 사용한다
  const locationName = item?.location?.name ?? "(unknown)";
  const temp = item?.latest?.temp;
  const weather =
    item?.latest?.weather_desc ??
    item?.latest?.weather_main ??
    "—";
  const observedAt = item?.latest?.observed_at ?? "";

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "220px 120px 1fr 220px",
        gap: 12,
        padding: "10px 10px",
        borderBottom: "1px solid #f3f4f6",
        alignItems: "center",
        fontSize: 14,
      }}
    >
      {/* Location + 상단등록(작게, 위첨자 느낌) */}
      <div style={{ fontWeight: 800, color: "#111827", minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 8, minWidth: 0 }}>
          <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {locationName}
          </span>

          <button
            type="button"
            onClick={onPromote}
            style={{
              border: "1px solid #c7d2fe",
              background: "#eef2ff",
              color: "#3730a3",
              borderRadius: 999,
              padding: "1px 6px",
              fontSize: 10,
              fontWeight: 900,
              cursor: "pointer",
              lineHeight: 1.2,
              position: "relative",
              top: -6, // ✅ 위첨자처럼
              whiteSpace: "nowrap",
            }}
            aria-label="Promote to top WeatherCard"
            title="상단에 등록"
          >
            상단등록
          </button>
        </div>
      </div>

      <div style={{ fontWeight: 900 }}>
        {temp === null || temp === undefined ? "--" : `${Math.round(Number(temp))}°`}
      </div>

      <div style={{ color: "#374151", overflow: "hidden", textOverflow: "ellipsis" }}>
        {String(weather)}
      </div>

      <div style={{ textAlign: "right", color: "#6b7280", fontSize: 12 }}>
        {observedAt ? fmtTimeStable(String(observedAt)) : ""}
      </div>
    </div>
  );
}