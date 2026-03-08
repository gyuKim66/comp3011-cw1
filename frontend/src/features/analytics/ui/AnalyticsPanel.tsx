// frontend/src/features/analytics/ui/AnalyticsPanel.tsx

"use client";

import { useEffect, useMemo, useState } from "react";

import {
  getHumidityStats,
  getTemperatureStats,
  getTemperatureTrend,
  type HumidityStats,
  type TemperatureStats,
  type TemperatureTrend,
} from "@/features/analytics/api";

type Props = {
  locationId: number;
  locationName?: string;
};

type RangeOption = "all" | "today" | "7d";

function formatValue(value: number | null, suffix = ""): string {
  if (value === null || value === undefined) return "-";
  return `${value}${suffix}`;
}

function resolveStatsDays(range: RangeOption): number | undefined {
  if (range === "all") return undefined;
  if (range === "today") return 0;
  return 7;
}

function resolveTrendDays(range: RangeOption): number {
  if (range === "today") return 1;
  if (range === "7d") return 7;
  return 7;
}

function rangeLabel(range: RangeOption): string {
  if (range === "all") return "All";
  if (range === "today") return "Today";
  return "7 days";
}

export default function AnalyticsPanel({ locationId, locationName }: Props) {
  const [range, setRange] = useState<RangeOption>("7d");
  const [tempStats, setTempStats] = useState<TemperatureStats | null>(null);
  const [humidityStats, setHumidityStats] = useState<HumidityStats | null>(null);
  const [trend, setTrend] = useState<TemperatureTrend | null>(null);

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const statsDays = resolveStatsDays(range);
  const trendDays = resolveTrendDays(range);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError(null);

      try {
        const [temp, humidity, trendData] = await Promise.all([
          getTemperatureStats(locationId, statsDays),
          getHumidityStats(locationId, statsDays),
          getTemperatureTrend(locationId, trendDays),
        ]);

        if (cancelled) return;

        setTempStats(temp);
        setHumidityStats(humidity);
        setTrend(trendData);
      } catch (e) {
        if (cancelled) return;
        setError(String(e));
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, [locationId, statsDays, trendDays]);

  const chartPoints = useMemo(() => {
    if (!trend?.data?.length) return [];

    const values = trend.data
      .map((x) => x.avg_temp)
      .filter((x): x is number => x !== null);

    if (values.length === 0) return [];

    const min = Math.min(...values);
    const max = Math.max(...values);
    const height = 120;
    const width = 320;
    const stepX = trend.data.length > 1 ? width / (trend.data.length - 1) : 0;

    return trend.data.map((point, index) => {
      const value = point.avg_temp;
      const x = index * stepX;

      let y = height / 2;
      if (value !== null) {
        if (max === min) {
          y = height / 2;
        } else {
          const ratio = (value - min) / (max - min);
          y = height - ratio * (height - 12) - 6;
        }
      }

      return {
        x,
        y,
        label: point.date,
        value,
      };
    });
  }, [trend]);

  const polylinePoints = useMemo(() => {
    if (!chartPoints.length) return "";
    return chartPoints.map((p) => `${p.x},${p.y}`).join(" ");
  }, [chartPoints]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 10,
        height: "100%",
        minHeight: 0,
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          gap: 10,
          flexWrap: "wrap",
        }}
      >
        <div>
          <div style={{ fontSize: 18, fontWeight: 900, color: "#111827" }}>
            Analytics{locationName ? ` – ${locationName}` : ""}
          </div>
          <div style={{ marginTop: 2, fontSize: 12, color: "#6b7280" }}>
            Temperature, humidity, and recent daily trend for the selected
            location.
          </div>
        </div>

        <div
          style={{
            display: "inline-flex",
            gap: 6,
            background: "#f3f4f6",
            padding: 4,
            borderRadius: 10,
          }}
        >
          {(["all", "today", "7d"] as RangeOption[]).map((option) => {
            const active = range === option;
            return (
              <button
                key={option}
                type="button"
                onClick={() => setRange(option)}
                style={{
                  border: "none",
                  borderRadius: 8,
                  padding: "6px 10px",
                  fontSize: 12,
                  fontWeight: 700,
                  cursor: "pointer",
                  background: active ? "#2563eb" : "transparent",
                  color: active ? "#ffffff" : "#374151",
                }}
              >
                {rangeLabel(option)}
              </button>
            );
          })}
        </div>
      </div>

      {loading ? (
        <div
          style={{
            flex: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#6b7280",
            fontSize: 13,
          }}
        >
          Analytics loading...
        </div>
      ) : error ? (
        <div
          style={{
            flex: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#b91c1c",
            background: "#fef2f2",
            border: "1px solid #fecaca",
            borderRadius: 12,
            padding: 12,
            fontSize: 13,
          }}
        >
          {error}
        </div>
      ) : (
        <>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
              gap: 10,
            }}
          >
            <div
              style={{
                background: "#f8fafc",
                border: "1px solid #e5e7eb",
                borderRadius: 12,
                padding: "10px 12px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                minHeight: 56,
              }}
            >
              <div style={{ fontSize: 13, color: "#6b7280", fontWeight: 700 }}>
                Avg Temp
              </div>
              <div
                style={{
                  fontSize: 20,
                  fontWeight: 900,
                  color: "#111827",
                  lineHeight: 1,
                }}
              >
                {formatValue(tempStats?.avg_temp ?? null, "°")}
              </div>
            </div>

            <div
              style={{
                background: "#f8fafc",
                border: "1px solid #e5e7eb",
                borderRadius: 12,
                padding: "10px 12px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                minHeight: 56,
              }}
            >
              <div style={{ fontSize: 13, color: "#6b7280", fontWeight: 700 }}>
                Min Temp
              </div>
              <div
                style={{
                  fontSize: 20,
                  fontWeight: 900,
                  color: "#111827",
                  lineHeight: 1,
                }}
              >
                {formatValue(tempStats?.min_temp ?? null, "°")}
              </div>
            </div>

            <div
              style={{
                background: "#f8fafc",
                border: "1px solid #e5e7eb",
                borderRadius: 12,
                padding: "10px 12px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                minHeight: 56,
              }}
            >
              <div style={{ fontSize: 13, color: "#6b7280", fontWeight: 700 }}>
                Max Temp
              </div>
              <div
                style={{
                  fontSize: 20,
                  fontWeight: 900,
                  color: "#111827",
                  lineHeight: 1,
                }}
              >
                {formatValue(tempStats?.max_temp ?? null, "°")}
              </div>
            </div>

            <div
              style={{
                background: "#f8fafc",
                border: "1px solid #e5e7eb",
                borderRadius: 12,
                padding: "10px 12px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                minHeight: 56,
              }}
            >
              <div style={{ fontSize: 13, color: "#6b7280", fontWeight: 700 }}>
                Avg Humidity
              </div>
              <div
                style={{
                  fontSize: 20,
                  fontWeight: 900,
                  color: "#111827",
                  lineHeight: 1,
                }}
              >
                {formatValue(humidityStats?.avg_humidity ?? null, "%")}
              </div>
            </div>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1.6fr 0.6fr",
              gap: 10,
              minHeight: 0,
            }}
          >
            <div
              style={{
                background: "#f8fafc",
                border: "1px solid #e5e7eb",
                borderRadius: 12,
                padding: 8,
                display: "flex",
                flexDirection: "column",
                minHeight: 0,
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: 6,
                }}
              >
                <div style={{ fontSize: 13, fontWeight: 800, color: "#111827" }}>
                  Temperature Trend
                </div>
                <div style={{ fontSize: 11, color: "#6b7280" }}>
                  Last {trendDays} day(s)
                </div>
              </div>

              {!trend?.data?.length ? (
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "#6b7280",
                    fontSize: 12,
                    height: 110,
                  }}
                >
                  No trend data available.
                </div>
              ) : (
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "3fr 1fr",
                    gap: 8,
                    minHeight: 0,
                    height: 140,
                    alignItems: "stretch",
                  }}
                >
                  <div
                    style={{
                      background: "#ffffff",
                      borderRadius: 10,
                      border: "1px solid #e5e7eb",
                      padding: 8,
                      display: "flex",
                      alignItems: "center",
                      height: 140,
                    }}
                  >
                    <svg
                      viewBox="0 0 320 120"
                      preserveAspectRatio="xMidYMid meet"
                      style={{ width: "100%", height: "100%" }}
                    >
                      <line
                        x1="0"
                        y1="118"
                        x2="100"
                        y2="118"
                        stroke="#d1d5db"
                        strokeWidth="1"
                      />
                      {polylinePoints ? (
                        <>
                          <polyline
                            fill="none"
                            stroke="#2563eb"
                            strokeWidth="2.2"
                            points={polylinePoints}
                          />
                          {chartPoints.map((point) => (
                            <circle
                              key={point.label}
                              cx={point.x}
                              cy={point.y}
                              r="2.4"
                              fill="#2563eb"
                            />
                          ))}
                        </>
                      ) : null}
                    </svg>
                  </div>

                  <div
                    style={{
                      overflowY: "auto",
                      paddingRight: 2,
                      height: 140,
                    }}
                  >
                    {trend.data.map((point) => (
                      <div
                        key={point.date}
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          gap: 6,
                          padding: "5px 0",
                          borderBottom: "1px solid #e5e7eb",
                          fontSize: 12,
                        }}
                      >
                        <span style={{ color: "#374151" }}>{point.date}</span>
                        <span style={{ fontWeight: 700, color: "#111827" }}>
                          {formatValue(point.avg_temp, "°")}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div
              style={{
                background: "#f8fafc",
                border: "1px solid #e5e7eb",
                borderRadius: 12,
                padding: 8,
                display: "flex",
                flexDirection: "column",
                gap: 8,
              }}
            >
              <div style={{ fontSize: 13, fontWeight: 800, color: "#111827" }}>
                Summary
              </div>

              <div
                style={{
                  background: "#ffffff",
                  border: "1px solid #e5e7eb",
                  borderRadius: 10,
                  padding: "8px 10px",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <span style={{ fontSize: 12, color: "#6b7280", fontWeight: 700 }}>
                  Count
                </span>
                <span style={{ fontSize: 16, fontWeight: 900, color: "#111827" }}>
                  {tempStats?.count ?? 0}
                </span>
              </div>

              <div
                style={{
                  background: "#ffffff",
                  border: "1px solid #e5e7eb",
                  borderRadius: 10,
                  padding: "8px 10px",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <span style={{ fontSize: 12, color: "#6b7280", fontWeight: 700 }}>
                  Temp Range
                </span>
                <span style={{ fontSize: 14, fontWeight: 800, color: "#111827" }}>
                  {formatValue(tempStats?.min_temp ?? null, "°")} ~{" "}
                  {formatValue(tempStats?.max_temp ?? null, "°")}
                </span>
              </div>

              <div
                style={{
                  background: "#ffffff",
                  border: "1px solid #e5e7eb",
                  borderRadius: 10,
                  padding: "8px 10px",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <span style={{ fontSize: 12, color: "#6b7280", fontWeight: 700 }}>
                  Active Range
                </span>
                <span style={{ fontSize: 14, fontWeight: 800, color: "#111827" }}>
                  {rangeLabel(range)}
                </span>
              </div>

            </div>
          </div>
        </>
      )}
    </div>
  );
}