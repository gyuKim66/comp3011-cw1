// frontend/src/features/home/ui/HomeClient.tsx


"use client";

import { useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";

import type { HomeResponse, HomeItemDTO } from "@/features/home/api";
import WeatherCard from "@/features/home/ui/WeatherCard";
import WeatherRow from "@/features/home/ui/WeatherRow";
import Toast from "@/features/home/ui/Toast";
import AddLocationBox from "@/features/locations/ui/AddLocationBox";
import { patchLocation } from "@/features/locations/api";

type Props = {
  initialData: HomeResponse;
};

export default function HomeClient({ initialData }: Props) {
  const router = useRouter();

  const [data] = useState<HomeResponse>(initialData);

  const initialFeatured: [HomeItemDTO | null, HomeItemDTO | null] = [
    data.featured?.[0] ?? null,
    data.featured?.[1] ?? null,
  ];

  const [featured, setFeatured] =
    useState<[HomeItemDTO | null, HomeItemDTO | null]>(initialFeatured);

  // optimistic list (새로 추가된 도시를 즉시 보이게)
  const [optimistic, setOptimistic] = useState<HomeItemDTO[]>([]);

  // Toast
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const toastTimer = useRef<number | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    if (toastTimer.current) window.clearTimeout(toastTimer.current);
    toastTimer.current = window.setTimeout(() => setToastMessage(null), 2500);
  };

  // list = (서버 list + optimistic) - featured
  const listItems = useMemo(() => {
    const base = [...optimistic, ...data.list];

    const featuredIds = new Set(
      featured.filter(Boolean).map((x) => (x as HomeItemDTO).location.id)
    );

    const seen = new Set<number>();
    const merged: HomeItemDTO[] = [];

    for (const it of base) {
      const id = it.location.id;
      if (featuredIds.has(id)) continue;
      if (seen.has(id)) continue;
      seen.add(id);
      merged.push(it);
    }
    return merged;
  }, [data.list, optimistic, featured]);

  // ✅ DB 반영 포함: 삭제(Featured 해제)
  const removeFeatured = async (index: 0 | 1) => {
    const target = featured[index];
    if (!target) return;

    const locId = target.location.id;

    try {
      await patchLocation(locId, { is_featured: false });

      // UI 재배치(왼쪽 삭제면 오른쪽이 왼쪽으로)
      setFeatured((prev) => {
        if (!prev[index]) return prev;
        if (index === 0) return [prev[1] ?? null, null];
        return [prev[0], null];
      });

      // 서버 스냅샷 재조회 → 아래 list로 내려오는 것도 여기서 확정
      router.refresh();
    } catch (e) {
      showToast(`삭제(Featured 해제) 실패: ${String(e)}`);
    }
  };

  // ✅ DB 반영 포함: 상단등록(Featured 설정)
  const promoteToFeatured = async (item: HomeItemDTO) => {
    const locId = item.location.id;

    // 이미 featured면 아무 것도 안 함
    const already =
      featured[0]?.location.id === locId || featured[1]?.location.id === locId;
    if (already) return;

    // UI 기준으로 2개 꽉 차있으면 서버 호출 전에 토스트
    if (featured[0] && featured[1]) {
      showToast("상단 WeatherCard는 최대 2개까지만 등록할 수 있습니다.");
      return;
    }

    try {
      await patchLocation(locId, { is_featured: true });

      // UI 즉시 반영(빈 슬롯에 넣기)
      setFeatured((prev) => {
        if (!prev[0]) return [item, prev[1]];
        if (!prev[1]) return [prev[0], item];
        return prev;
      });

      // 서버 스냅샷 재조회(정렬/featured 제외 list 재계산 포함)
      router.refresh();
    } catch (e) {
      const msg = String(e);
      if (msg.includes("409")) {
        showToast("이미 상단 등록이 2개입니다. 다른 카드를 먼저 삭제하세요.");
        return;
      }
      showToast(`상단 등록 실패: ${msg}`);
    }
  };

  // AddLocationBox에서 최신값까지 포함해 즉시 업데이트
  const onCreated = (payload: any) => {
    const loc = payload?.location ?? payload;
    const latest = payload?.latest ?? null;
    const id = loc?.id;

    if (id === undefined || id === null) {
      showToast("추가한 location 데이터가 올바르지 않습니다.");
      return;
    }

    setOptimistic((prev) => {
      const exists = prev.some((x) => x.location.id === id);
      if (!exists) return [{ location: loc, latest }, ...prev];
      return prev.map((x) => (x.location.id === id ? { location: loc, latest } : x));
    });
  };

  return (
    <>
      <main
        style={{
          height: "100vh",
          display: "grid",
          gridTemplateRows: "auto 1fr",
          gap: 14,
          padding: 18,
          background: "#f3f4f6",
          fontFamily:
            "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
        }}
      >
        {/* 상단 2-card */}
        <section
          style={{
            background: "#ffffff",
            borderRadius: 16,
            padding: 18,
            boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
          }}
        >
          <h1 style={{ fontSize: 22, fontWeight: 900, marginBottom: 12 }}>
            Featured Locations
          </h1>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 14,
            }}
          >
            <div>
              {featured[0] ? (
                <WeatherCard
                  item={featured[0]}
                  variant="default"
                  onDelete={() => removeFeatured(0)}
                />
              ) : (
                <div style={{ color: "#6b7280" }}>비어 있습니다.</div>
              )}
            </div>

            <div>
              {featured[1] ? (
                <WeatherCard
                  item={featured[1]}
                  variant="secondary"
                  onDelete={() => removeFeatured(1)}
                />
              ) : (
                <div style={{ color: "#6b7280" }}>비어 있습니다.</div>
              )}
            </div>
          </div>
        </section>

        {/* 하단 리스트 */}
        <section
          style={{
            background: "#ffffff",
            borderRadius: 16,
            padding: 18,
            overflowY: "auto",
            boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
            display: "grid",
            gap: 12,
          }}
        >
          <h2 style={{ fontSize: 18, fontWeight: 900 }}>My Locations</h2>

          <AddLocationBox
            toast={showToast}
            onCreated={onCreated}
            onDone={() => router.refresh()}
          />

          {/* 리스트 헤더 */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "220px 120px 1fr 220px",
              gap: 12,
              padding: "10px 10px",
              borderBottom: "1px solid #e5e7eb",
              color: "#6b7280",
              fontSize: 12,
              fontWeight: 800,
            }}
          >
            <div>Location</div>
            <div>Temp</div>
            <div>Weather</div>
            <div style={{ textAlign: "right" }}>Observed at</div>
          </div>

          {/* 리스트 바디 */}
          <div>
            {listItems.map((item) => (
              <WeatherRow
                key={item.location.id}
                item={item}
                onPromote={() => promoteToFeatured(item)}
              />
            ))}
          </div>
        </section>
      </main>

      <Toast message={toastMessage} />
    </>
  );
}