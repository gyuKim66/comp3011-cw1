// frontend/src/features/home/ui/Toast.tsx



"use client";

type Props = {
  message: string | null;
};

export default function Toast({ message }: Props) {
  if (!message) return null;

  return (
    <div
      style={{
        position: "fixed",
        bottom: 24,
        left: "50%",
        transform: "translateX(-50%)",
        background: "#111827",
        color: "#ffffff",
        padding: "10px 14px",
        borderRadius: 10,
        fontSize: 13,
        fontWeight: 800,
        boxShadow: "0 10px 24px rgba(0,0,0,0.18)",
        zIndex: 9999,
        maxWidth: "calc(100vw - 48px)",
        whiteSpace: "nowrap",
        overflow: "hidden",
        textOverflow: "ellipsis",
      }}
    >
      {message}
    </div>
  );
}