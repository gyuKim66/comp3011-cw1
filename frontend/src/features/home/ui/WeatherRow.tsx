// frontend/src/features/home/ui/WeatherRow.tsx

"use client";

import { deleteLocation } from "@/features/locations/api";

type Props = {
  item: any;
  onPromote: () => void;

  // ✅ HomeClient에서 router.refresh()를 연결할 콜백
  onDeleted?: () => void;

  // ✅ 하단 목록에서만 Delete 버튼 노출
  showDelete?: boolean;

  // (선택) 토스트
  toast?: (msg: string) => void;
};

function fmtTimeStable(iso: string) {
  const d = new Date(iso);
  if (isNaN(d.getTime())) return iso;
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  const hh = String(d.getHours()).padStart(2, "0");
  const mi = String(d.getMinutes()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd} ${hh}:${mi}`;
}

export default function WeatherRow({
  item,
  onPromote,
  onDeleted,
  showDelete = false,
  toast,
}: Props) {
  const locationName = item?.location?.name ?? "(unknown)";
  const temp = item?.latest?.temp;
  const weather = item?.latest?.weather_desc ?? item?.latest?.weather_main ?? "—";
  const observedAt = item?.latest?.observed_at ?? "";

  const onDelete = async () => {
    const id = item?.location?.id;
    if (id === undefined || id === null) {
      toast?.("삭제할 location id가 없습니다.");
      return;
    }

    try {
      await deleteLocation(Number(id)); // ✅ DELETE /locations/{id}
      toast?.("삭제되었습니다. (비활성화)");
      onDeleted?.(); // ✅ HomeClient에서 router.refresh()
    } catch (e) {
      toast?.(`삭제 실패: ${String(e)}`);
    }
  };

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: showDelete ? "220px 120px 1fr 160px 90px" : "220px 120px 1fr 220px",
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
              top: -6,
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

      {/* ✅ Delete 버튼은 하단 목록에서만 표시 */}
      {showDelete ? (
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <button
            type="button"
            onClick={onDelete}
            style={{
              border: "1px solid #fecaca",
              background: "#fff",
              color: "#991b1b",
              borderRadius: 10,
              padding: "6px 10px",
              fontSize: 12,
              fontWeight: 900,
              cursor: "pointer",
              whiteSpace: "nowrap",
            }}
            aria-label="Delete (soft delete) location"
            title="목록에서 삭제(비활성화)"
          >
            Delete
          </button>
        </div>
      ) : null}
    </div>
  );
}