// frontend/src/features/locations/ui/AddLocationBox.tsx


"use client";

import { useEffect, useRef, useState } from "react";
import { createLocation, searchLocations, type Location, type LocationSearchItem } from "@/features/locations/api";
import { fetchObservation, getLatestObservation, type LatestObservationDTO } from "@/features/observations/api";

type Props = {
  onDone: () => void;
  toast: (msg: string) => void;

  // ✅ created만이 아니라 latest까지 반영할 수 있게 payload 확장
  onCreated?: (item: { location: Location; latest: LatestObservationDTO | null }) => void;
};

export default function AddLocationBox({ onDone, toast, onCreated }: Props) {
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [items, setItems] = useState<LocationSearchItem[]>([]);
  const [selected, setSelected] = useState<LocationSearchItem | null>(null);

  const debounceRef = useRef<number | null>(null);

  useEffect(() => {
    setSelected(null);

    if (q.trim().length < 2) {
      setItems([]);
      return;
    }

    if (debounceRef.current) window.clearTimeout(debounceRef.current);
    debounceRef.current = window.setTimeout(async () => {
      setLoading(true);
      try {
        const res = await searchLocations(q.trim(), 6);
        setItems(res);
      } catch (e) {
        toast(`검색 실패: ${String(e)}`);
        setItems([]);
      } finally {
        setLoading(false);
      }
    }, 350);

    return () => {
      if (debounceRef.current) window.clearTimeout(debounceRef.current);
    };
  }, [q, toast]);

  const add = async () => {
    if (!selected) {
      toast("먼저 검색 결과에서 도시를 선택해 주세요.");
      return;
    }

    try {
      // 1) location 저장
      const created = await createLocation({
        name: selected.name,
        country_code: selected.country_code,
        lat: selected.lat,
        lon: selected.lon,
        is_active: true,
        is_featured: false,
      });

      // ✅ 2) 즉시 리스트에 추가(일단 latest는 null)
      onCreated?.({ location: created, latest: null });

      // 3) observation fetch (DB 저장)
      await fetchObservation(created.id);

      // 4) 최신 observation 다시 조회해서 UI 업데이트
      const latest = await getLatestObservation(created.id);
      onCreated?.({ location: created, latest });

      toast("추가 완료!");
      setQ("");
      setItems([]);
      setSelected(null);

      // 5) 최종 동기화(/home 재조회)
      onDone();
    } catch (e) {
      const msg = String(e);
      if (msg.includes("409")) {
        toast("이미 등록된 도시입니다.");
        return;
      }
      toast(`추가 실패: ${msg}`);
    }
  };

  return (
    <div
      style={{
        border: "1px solid #e5e7eb",
        borderRadius: 14,
        padding: 12,
        display: "grid",
        gap: 10,
        background: "#ffffff",
      }}
    >
      <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="도시명 검색 (예: Busan, Tokyo)"
          style={{
            flex: 1,
            border: "1px solid #e5e7eb",
            borderRadius: 10,
            padding: "10px 12px",
            fontSize: 14,
            outline: "none",
          }}
        />
        <button
          type="button"
          onClick={add}
          disabled={!selected}
          style={{
            border: "1px solid #111827",
            background: selected ? "#111827" : "#9ca3af",
            color: "#fff",
            borderRadius: 10,
            padding: "10px 12px",
            fontSize: 13,
            fontWeight: 900,
            cursor: selected ? "pointer" : "not-allowed",
            whiteSpace: "nowrap",
          }}
        >
          추가
        </button>
      </div>

      <div style={{ fontSize: 12, color: "#6b7280", fontWeight: 700 }}>
        {loading ? "검색 중..." : selected ? "선택됨" : "검색 후 항목을 선택하세요"}
      </div>

      {items.length > 0 ? (
        <div style={{ display: "grid", gap: 6 }}>
          {items.map((it, idx) => {
            const label = `${it.name}${it.state ? `, ${it.state}` : ""} (${it.country_code})`;
            const active = selected && selected.lat === it.lat && selected.lon === it.lon;

            return (
              <button
                key={`${it.name}-${it.lat}-${it.lon}-${idx}`}
                type="button"
                onClick={() => setSelected(it)}
                style={{
                  textAlign: "left",
                  border: "1px solid #e5e7eb",
                  background: active ? "#eef2ff" : "#fff",
                  borderRadius: 10,
                  padding: "10px 12px",
                  cursor: "pointer",
                  display: "grid",
                  gap: 4,
                }}
              >
                <div style={{ fontSize: 14, fontWeight: 900, color: "#111827" }}>
                  {label}
                </div>
                <div style={{ fontSize: 12, color: "#6b7280" }}>
                  lat {it.lat.toFixed(4)}, lon {it.lon.toFixed(4)}
                </div>
              </button>
            );
          })}
        </div>
      ) : null}
    </div>
  );
}