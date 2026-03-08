// frontend/src/features/home/ui/HomeClient.tsx

"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";

import type { HomeResponse, HomeItemDTO } from "@/features/home/api";
import WeatherCard from "@/features/home/ui/WeatherCard";
import WeatherRow from "@/features/home/ui/WeatherRow";
import Toast from "@/features/home/ui/Toast";
import AddLocationBox from "@/features/locations/ui/AddLocationBox";
import { patchLocation } from "@/features/locations/api";
import AnalyticsPanel from "@/features/analytics/ui/AnalyticsPanel";

type Props = {
  initialData: HomeResponse;
};

export default function HomeClient({ initialData }: Props) {
  const router = useRouter();
  const data = initialData;

  const initialFeatured: [HomeItemDTO | null, HomeItemDTO | null] = [
    data.featured?.[0] ?? null,
    data.featured?.[1] ?? null,
  ];

  const [featured, setFeatured] =
    useState<[HomeItemDTO | null, HomeItemDTO | null]>(initialFeatured);

  const [optimistic, setOptimistic] = useState<HomeItemDTO[]>([]);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [selectedLocationId, setSelectedLocationId] = useState<number | null>(
    null
  );

  const toastTimer = useRef<number | null>(null);

  useEffect(() => {
    setFeatured(initialFeatured);
  }, [data.featured?.[0]?.location.id, data.featured?.[1]?.location.id]);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    if (toastTimer.current) window.clearTimeout(toastTimer.current);
    toastTimer.current = window.setTimeout(() => setToastMessage(null), 2500);
  };

  const listItems = useMemo(() => {
    const base = [...optimistic, ...data.list];

    const featuredIds = new Set(
      featured.filter(Boolean).map((x) => (x as HomeItemDTO).location.id)
    );

    const seen = new Set<number>();
    const merged: HomeItemDTO[] = [];

    for (const it of base) {
      const id = it.location.id;

      if (!it.location.is_active) continue;
      if (featuredIds.has(id)) continue;
      if (seen.has(id)) continue;

      seen.add(id);
      merged.push(it);
    }

    return merged;
  }, [data.list, optimistic, featured]);

  useEffect(() => {
    if (selectedLocationId !== null) return;

    if (featured[0]?.location.id) {
      setSelectedLocationId(featured[0].location.id);
      return;
    }

    if (featured[1]?.location.id) {
      setSelectedLocationId(featured[1].location.id);
      return;
    }

    if (listItems.length > 0) {
      setSelectedLocationId(listItems[0].location.id);
    }
  }, [featured, listItems, selectedLocationId]);

  const removeFeatured = async (index: 0 | 1) => {
    const target = featured[index];
    if (!target) return;

    const locId = target.location.id;

    try {
      await patchLocation(locId, { is_featured: false });

      if (index === 0 && featured[1]) {
        await patchLocation(featured[1].location.id, {
          is_featured: true,
          display_order: 0,
        });
      }

      setFeatured((prev) => {
        if (!prev[index]) return prev;
        if (index === 0) return [prev[1] ?? null, null];
        return [prev[0], null];
      });

      if (selectedLocationId === locId) {
        const fallbackId =
          index === 0
            ? featured[1]?.location.id ?? null
            : featured[0]?.location.id ?? null;

        setSelectedLocationId(fallbackId);
      }

      router.refresh();
    } catch (e) {
      showToast(`삭제(Featured 해제) 실패: ${String(e)}`);
    }
  };

  const promoteToFeatured = async (item: HomeItemDTO) => {
    const locId = item.location.id;

    const already =
      featured[0]?.location.id === locId || featured[1]?.location.id === locId;
    if (already) return;

    if (featured[0] && featured[1]) {
      showToast("상단 WeatherCard는 최대 2개까지만 등록할 수 있습니다.");
      return;
    }

    try {
      if (!featured[0]) {
        await patchLocation(locId, {
          is_featured: true,
          display_order: 0,
        });
        setFeatured((prev) => [item, prev[1]]);
      } else if (!featured[1]) {
        await patchLocation(locId, {
          is_featured: true,
          display_order: 1,
        });
        setFeatured((prev) => [prev[0], item]);
      }

      router.refresh();
    } catch (e) {
      showToast(`상단 등록 실패: ${String(e)}`);
    }
  };

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
      return prev.map((x) =>
        x.location.id === id ? { location: loc, latest } : x
      );
    });

    if (selectedLocationId === null) {
      setSelectedLocationId(id);
    }
  };

  return (
    <>
      <main
        style={{
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          gap: 14,
          padding: 18,
          background: "#f3f4f6",
          fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
        }}
      >
        {/* Header */}
        <section
          style={{
            background: "linear-gradient(135deg,#0f172a,#1e293b)",
            color: "#fff",
            borderRadius: 18,
            padding: "22px 24px",
            boxShadow: "0 6px 18px rgba(0,0,0,0.10)",
          }}
        >
          <div style={{ fontSize: 28, fontWeight: 900 }}>
            Climate & Weather Analytics Dashboard
          </div>
          <div style={{ marginTop: 8, fontSize: 14, color: "#cbd5e1" }}>
            Monitor featured cities, manage locations, and explore analytics.
          </div>
        </section>

        {/* Featured */}
        <section
          style={{
            background: "#fff",
            borderRadius: 16,
            padding: 18,
            boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
          }}
        >
          <h1 style={{ fontSize: 22, fontWeight: 900, marginBottom: 12 }}>
            Featured Locations
          </h1>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
            {featured.map((item, idx) => {
              const isSelected = selectedLocationId === item?.location.id;

              return (
                <div
                  key={idx}
                  onClick={() => item && setSelectedLocationId(item.location.id)}
                  style={{
                    cursor: item ? "pointer" : "default",
                    border: isSelected
                      ? "2px solid #2563eb"
                      : "2px solid transparent",
                    borderRadius: 16,
                    transition: "all 0.15s ease",
                  }}
                >
                  {item ? (
                    <WeatherCard
                      item={item}
                      variant={idx === 0 ? "default" : "secondary"}
                      onDelete={() => removeFeatured(idx as 0 | 1)}
                    />
                  ) : (
                    <div style={{ color: "#6b7280" }}>비어 있습니다.</div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* My Locations */}
        <section
          style={{
            background: "#fff",
            borderRadius: 16,
            padding: 18,
            boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
          }}
        >
          <h2 style={{ fontSize: 18, fontWeight: 900 }}>My Locations</h2>

          <AddLocationBox
            toast={showToast}
            onCreated={onCreated}
            onDone={() => router.refresh()}
          />

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "220px 120px 1fr 160px 90px",
              gap: 12,
              padding: "10px",
              borderBottom: "1px solid #e5e7eb",
              fontSize: 12,
              fontWeight: 800,
            }}
          >
            <div>Location</div>
            <div>Temp</div>
            <div>Weather</div>
            <div style={{ textAlign: "right" }}>Observed at</div>
            <div style={{ textAlign: "right" }}>Delete</div>
          </div>

          <div style={{ display: "flex", flexDirection: "column", paddingRight: 4 }}>
            {listItems.map((item) => {
              const isSelected = selectedLocationId === item.location.id;

              return (
                <div
                  key={item.location.id}
                  onClick={() => setSelectedLocationId(item.location.id)}
                  style={{
                    cursor: "pointer",
                    borderRadius: 12,
                    background: isSelected ? "#eff6ff" : "transparent",
                    border: isSelected
                      ? "1px solid #bfdbfe"
                      : "1px solid transparent",
                    flexShrink: 0,
                    transition: "all 0.15s ease",
                  }}
                >
                  <WeatherRow
                    item={item}
                    onPromote={() => promoteToFeatured(item)}
                    showDelete
                    onDeleted={() => {
                      const deletedId = item.location.id;

                      setOptimistic((prev) =>
                        prev.filter((x) => x.location.id !== deletedId)
                      );

                      if (selectedLocationId === deletedId) {
                        setSelectedLocationId(null);
                      }

                      router.refresh();
                    }}
                    toast={showToast}
                  />
                </div>
              );
            })}
          </div>
        </section>

        {/* Analytics */}
        <section
          style={{
            background: "#fff",
            borderRadius: 16,
            padding: 18,
            boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
          }}
        >
          {selectedLocationId ? (
            <AnalyticsPanel
              locationId={selectedLocationId}
              locationName={
                featured[0]?.location.id === selectedLocationId
                  ? featured[0]?.location.name
                  : featured[1]?.location.id === selectedLocationId
                  ? featured[1]?.location.name
                  : listItems.find((x) => x.location.id === selectedLocationId)
                      ?.location.name
              }
            />
          ) : (
            <div style={{ color: "#6b7280" }}>선택된 도시가 없습니다.</div>
          )}
        </section>
      </main>

      <Toast message={toastMessage} />
    </>
  );
}