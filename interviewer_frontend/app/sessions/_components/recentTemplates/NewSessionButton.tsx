
"use client";

export default function NewSessionButton() {
  return (
    <button
      style={{
        width: "100%",
        height: "100px",
        backgroundColor: "#C7A4F5",
        border: "none",
        borderRadius: "12px",
        padding: "20px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        color: "#2D2535",
        cursor: "pointer",
        transition: "transform 0.2s ease",
      }}
      onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.02)")}
      onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
      onClick={() => alert("New Session modal will open later")}
    >
      <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start" }}>
        <h3 style={{ marginBottom: "4px", fontSize: "18px", fontWeight: "700" }}>
          New Session
        </h3>
        <p style={{ fontSize: "14px", color: "#4B3F57" }}>
          Start a new session with a curated template
        </p>
      </div>

      {/* Plus Icon */}
      <div
        style={{
          backgroundColor: "#2D2535",
          borderRadius: "50%",
          width: "28px",
          height: "28px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path d="M12 5v14m-7-7h14" stroke="white" strokeWidth="2" strokeLinecap="round" />
        </svg>
      </div>
    </button>
  );
}
