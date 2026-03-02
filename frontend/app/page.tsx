import WeatherCard from "@/features/home/ui/WeatherCard";
import WeatherRow from "@/features/home/ui/WeatherRow";
import { getHome } from "@/features/home/api";


export default async function HomePage() {
  const data = await getHome();

  return (
    <main
      style={{
        height: "100vh",
        display: "grid",
        gridTemplateRows: "auto 1fr",
        gap: 14,
        padding: 18,
        background: "#f3f4f6",
        fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
      }}
    >
      {/* ✅ 상단 프레임: 왼쪽 50%만 사용 + 오른쪽 비움 */}
      <section
        style={{
          background: "#ffffff",
          borderRadius: 16,
          padding: 18,
          boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
        }}
      >
        <h1 style={{ fontSize: 22, fontWeight: 900, marginBottom: 12 }}>
          Default Location
        </h1>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          {/* left half */}
          <div>
            {data.default ? (
              <WeatherCard item={data.default} variant="default" />
            ) : (
              <div style={{ color: "#6b7280" }}>default location이 없습니다.</div>
            )}
          </div>

          {/* right half (empty) */}
          <div />
        </div>
      </section>

      {/* ✅ 하단 프레임: 카드 대신 리스트 */}
      <section
        style={{
          background: "#ffffff",
          borderRadius: 16,
          padding: 18,
          overflowY: "auto",
          boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
        }}
      >
        <h2 style={{ fontSize: 18, fontWeight: 900, marginBottom: 10 }}>
          My Locations
        </h2>

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
          {data.list.map((item) => (
            <WeatherRow key={item.location.id} item={item} />
          ))}
        </div>
      </section>
    </main>
  );
}