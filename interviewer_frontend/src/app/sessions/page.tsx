import styles from "./page.module.css";
import PastSessionsGrid from "./_components/pastSessions/pastSessions";

function SessionPage() {
  return (
    <div className={styles.sessionPageContainer}>
      {/* Remove this and replace with recent templates component */}
      <section className={styles.recentTemplatesContainer}></section>

      {/* remove this component and replace with past sessions component */}
      <section className={styles.pastSessionsContainer}>
        <PastSessionsGrid />
      </section>
    </div>
  );
}

export default SessionPage;
