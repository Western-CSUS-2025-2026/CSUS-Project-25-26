"use client";

type Template = {
  id: number;
  title: string;
  description: string;
};

export default function RecentTemplateCard({ template }: { template: Template }) {
  return (
    <div
      style={{
        flex: "1",
        backgroundColor: "#181818",
        border: "1px solid #2D2D2D",
        borderRadius: "12px",
        padding: "20px",
        height: "100px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        color: "#FFFFFF",
        transition: "transform 0.2s ease",
        cursor: "pointer",
      }}
      onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.02)")}
      onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
    >
      <div>
        <h3 style={{ marginBottom: "4px", fontSize: "18px", fontWeight: "700" }}>
          {template.title}
        </h3>
        <p style={{ fontSize: "14px", color: "#8D8D8D" }}>{template.description}</p>
      </div>

      {/* Plus Icon */}
      <div
        style={{
          backgroundColor: "#C7A4F5",
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
          <path d="M12 5v14m-7-7h14" stroke="#2D2535" strokeWidth="2" strokeLinecap="round" />
        </svg>
      </div>
    </div>
  );
}
