import { getRecentTemplates } from "@/lib/recentTemplates";
import TemplateCard from "./templateCard";
import NewSessionButton from "./NewSessionButton";


export default async function RecentTemplates() {
  const templates = await getRecentTemplates();

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        gap: "1.5rem",
        width: "100%",
      }}
    >
      {/* LEFT SECTION — NEW SESSION */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        <h2 style={{ margin: 0 }}>New Session</h2>
        <NewSessionButton />
      </div>

      {/* RIGHT SECTION — RECENT TEMPLATES */}
      <div style={{ flex: 2, display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        <h2 style={{ margin: 0 }}>Recent Templates</h2>

        <div style={{ display: "flex", flexDirection: "row", gap: "1rem" }}>
          {templates.map((t, i) => (
            <TemplateCard key={`${t.id}-${i}`} template={t} />
          ))}
        </div>
      </div>
    </div>
  );
}
