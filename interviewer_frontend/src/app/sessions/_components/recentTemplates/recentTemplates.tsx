import { getRecentTemplates } from "@/lib/recentTemplates";
import TemplateCard from "./templateCard";
import NewSessionButton from "./NewSessionButton";

// Layout section for New Session + Recent Templates
export default async function RecentTemplates() {
  const templates = await getRecentTemplates(); // fetch recent templates

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        gap: "1.5rem",
        width: "100%",
      }}
    >
      {/* Left column — New Session */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        <h2 style={{ margin: 0 }}>New Session</h2>
        <NewSessionButton />
      </div>

      {/* Right column — Recent Templates */}
      <div style={{ flex: 2, display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        <h2 style={{ margin: 0 }}>Recent Templates</h2>

        {/* Row of template cards */}
        <div style={{ display: "flex", flexDirection: "row", gap: "1rem" }}>
          {templates.map((t, i) => (
            <TemplateCard key={`${t.id}-${i}`} template={t} />
          ))}
        </div>
      </div>
    </div>
  );
}
