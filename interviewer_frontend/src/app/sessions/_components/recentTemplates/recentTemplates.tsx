import { Suspense } from "react";
import { getRecentTemplates } from "@/lib/recentTemplates";
import TemplateCard from "./templateCard";
import NewSessionButton from "./NewSessionButton";
import LoadingTemplateCard from "./loadingTemplateCard"; 


async function RecentTemplatesContent() {
  const templates = await getRecentTemplates(); // fetch recent templates

  return (
    <div style={{ display: "flex", flexDirection: "row", gap: "1rem" }}>
      {templates.map((t, i) => (
        <TemplateCard key={`${t.id}-${i}`} template={t} />
      ))}
    </div>
  );
}

// Main component with Suspense + Loading State
export default function RecentTemplates() {
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
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          gap: "0.75rem",
        }}
      >
        <h2 style={{ margin: 0 }}>New Session</h2>
        <NewSessionButton />
      </div>

      {/* Right column — Recent Templates */}
      <div
        style={{
          flex: 2,
          display: "flex",
          flexDirection: "column",
          gap: "0.75rem",
        }}
      >
        <h2 style={{ margin: 0 }}>Recent Templates</h2>

        <Suspense
          fallback={
            <div style={{ display: "flex", flexDirection: "row", gap: "1rem" }}>
              <LoadingTemplateCard />
              <LoadingTemplateCard />
            </div>
          }
        >
          <RecentTemplatesContent />
        </Suspense>
      </div>
    </div>
  );
}
