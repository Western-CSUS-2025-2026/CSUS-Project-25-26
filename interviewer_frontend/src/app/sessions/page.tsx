import styles from "./page.module.css";
import RecentTemplates from "./_components/recentTemplates/recentTemplates";


function SessionPage() {
  return (
    <div className={styles.sessionPageContainer}>
      {/* Remove this and replace with recent templates component */}
      <section className={styles.recentTemplatesContainer}>
        <RecentTemplates />
      </section>


      {/* remove this component and replace with past sessions component */}
      <section className={styles.pastSessionsContainer}></section>
    </div>
  );
}

export default SessionPage;
