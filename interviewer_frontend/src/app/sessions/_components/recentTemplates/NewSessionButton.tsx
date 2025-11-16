"use client";

export default function NewSessionButton() {
  return (
    <button
      style={{
        width: "100%",
        height: "100px",
        backgroundColor: "var(--accent)",
        border: "none",
        borderRadius: "12px",
        padding: "1.25rem",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        color: "var(--accent-primary-text)",
        cursor: "pointer",
        transition: "transform 0.2s ease",
        textAlign: "left",
      }}
      onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.02)")}
      onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
      onClick={() => alert("New Session modal will open soon")}
    >
      <div style={{ display: "flex", flexDirection: "column" }}>
        <h3 style={{ margin: 0 }}>New Session</h3>
        <p style={{ margin: 0, color: "var(--accent-secondary-text)" }}>
          Start a new session with a curated template
        </p>
      </div>

      {/* Plus Icon */}
      <div
        style={{
          backgroundColor: "var(--accent-primary-text)",
          borderRadius: "50%",
          width: "28px",
          height: "28px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
          <path
            d="M12 5v14m-7-7h14"
            stroke="var(--primary-text)"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
      </div>
    </button>
  );
}
