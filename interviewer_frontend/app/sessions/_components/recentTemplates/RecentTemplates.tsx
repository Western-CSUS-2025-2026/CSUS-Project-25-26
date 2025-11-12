import RecentTemplateCard from "./RecentTemplateCard";
import NewSessionButton from "./NewSessionButton";
import { getRecentTemplates } from "@/lib/recentTemplates"; 
import { Template } from "@/types/template";

export default async function RecentTemplates() {
  
  const templates: Template[] = await getRecentTemplates();

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
