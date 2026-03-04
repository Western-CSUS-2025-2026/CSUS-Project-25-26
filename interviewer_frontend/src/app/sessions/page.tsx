import styles from "./page.module.css";
import PastSessionsGrid from "./_components/pastSessions/pastSessions";
import RecentTemplates from "./_components/recentTemplates/recentTemplates";

import { getTemplates } from "@/lib/getTemplates";
import NewSessionModal from "./_components/newSessionModal/NewSessionModal";

export default async function SessionPage() {
  const templates = await getTemplates(); // fetch once on page load

  return (
    <div className={styles.sessionPageContainer}>
      <section className={styles.recentTemplatesContainer}>
        <RecentTemplates />
      </section>

      <section className={styles.pastSessionsContainer}>
        <PastSessionsGrid />
      </section>

      {/* Client-controlled modal instant open/close */}
      <NewSessionModal templates={templates} />
    </div>
  );
}
