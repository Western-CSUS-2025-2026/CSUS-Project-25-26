import { Suspense } from "react";
import styles from "./recentTemplates.module.css";
import { getRecentTemplates } from "@/lib/recentTemplates";
import TemplateCard from "./templateCard/templateCard";
import LoadingTemplateCard from "./loadingTemplateCard/loadingTemplateCard";
import NewSessionCard from "./newSessionButton/NewSessionCard";

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
    <div className={styles.container}>
      {/* Left column — New Session */}
      <div className={`${styles.innerContainer} ${styles.flex1}`}>
        <h2>New Session</h2>
        <NewSessionCard></NewSessionCard>
      </div>

      {/* Right column — Recent Templates */}
      <div className={`${styles.innerContainer} ${styles.flex2}`}>
        <h2>Recent Templates</h2>

        <Suspense fallback={<LoadingCards></LoadingCards>}>
          <RecentTemplatesContent />
        </Suspense>
      </div>
    </div>
  );
}

function LoadingCards() {
  return (
    <div className={styles.loadingCardsContainer}>
      <LoadingTemplateCard></LoadingTemplateCard>
      <LoadingTemplateCard></LoadingTemplateCard>
    </div>
  );
}
