"use client";

import { useState } from "react";
import { getHealth } from "@/features/health/api";

export default function Home() {
  const [result, setResult] = useState<string>("(아직 호출 안 함)");
  const [loading, setLoading] = useState<boolean>(false);

  const callHealth = async () => {
    setLoading(true);
    setResult("요청 중...");

    try {
      const data = await getHealth();
      setResult(JSON.stringify(data, null, 2));
    } catch (e) {
      setResult(`에러: ${String(e)}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: 22, fontWeight: 700 }}>
        Frontend ↔ Backend 연결 테스트
      </h1>

      <button
        onClick={callHealth}
        disabled={loading}
        style={{
          marginTop: 12,
          padding: "10px 14px",
          borderRadius: 8,
          border: "1px solid #ccc",
          cursor: "pointer",
        }}
      >
        {loading ? "Calling..." : "Call /health"}
      </button>

      <pre
        style={{
          marginTop: 16,
          padding: 12,
          background: "#f6f6f6",
          borderRadius: 8,
          overflowX: "auto",
        }}
      >
        {result}
      </pre>
    </main>
  );
}
