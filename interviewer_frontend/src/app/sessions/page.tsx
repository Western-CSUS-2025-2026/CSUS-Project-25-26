import styles from "./page.module.css";
import PastSessionsGrid from "./_components/pastSessions/pastSessions";
import RecentTemplates from "./_components/recentTemplates/recentTemplates";
import NewSessionModal from "./_components/newSessionModal/NewSessionModal";

type SearchParamProps = {
  searchParams: Record<string, string> | null | undefined;
};

async function SessionPage({ searchParams }: SearchParamProps) {
  const resolvedParams = await searchParams;

  return (
    <div className={styles.sessionPageContainer}>
      {/* Recent templates bar */}
      <section className={styles.recentTemplatesContainer}>
        <RecentTemplates />
      </section>

      {/* Past sessions grid */}
      <section className={styles.pastSessionsContainer}>
        <PastSessionsGrid />
      </section>

      {/* URL-driven template select modal */}
      <NewSessionModal searchParams={resolvedParams} />
    </div>
  );
}

export default SessionPage;
