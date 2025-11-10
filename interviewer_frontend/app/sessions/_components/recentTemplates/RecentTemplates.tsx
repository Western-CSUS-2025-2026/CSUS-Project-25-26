import RecentTemplateCard from "./RecentTemplateCard";
import NewSessionButton from "./NewSessionButton";

// Simulate fetching recent templates from the backend
async function getRecentTemplates() {
  await new Promise((r) => setTimeout(r, 2000));
  return [
    { id: 1, title: "SWE Internship", description: "Software Engineer Internship template" },
    { id: 2, title: "SWE Internship", description: "Software Engineer Internship template" },
  ];
}

export default async function RecentTemplates() {
  const templates = await getRecentTemplates();

  return (
    <section
      style={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "center",
        alignItems: "flex-start",
        gap: "24px",
        width: "1490px",
        margin: "60px auto",
      }}
    >
      {/* === LEFT: New Session === */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "16px",
          width: "30%",
        }}
      >
        <h2
          style={{
            fontSize: "24px",
            fontWeight: 700,
            color: "#ffffff",
            marginLeft: "4px",
          }}
        >
          New Session
        </h2>
        <NewSessionButton />
      </div>

      {/* === RIGHT: Recent Templates === */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "16px",
          width: "65%",
        }}
      >
        <h2
          style={{
            fontSize: "24px",
            fontWeight: 700,
            color: "#ffffff",
            marginLeft: "4px",
          }}
        >
          Recent Templates
        </h2>

        <div
          style={{
            display: "flex",
            flexDirection: "row",
            gap: "16px",
          }}
        >
          {templates.map((t) => (
            <RecentTemplateCard key={t.id} template={t} />
          ))}
        </div>
      </div>
    </section>
  );
}
