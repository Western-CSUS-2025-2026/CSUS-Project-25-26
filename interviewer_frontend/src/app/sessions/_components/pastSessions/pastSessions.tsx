import { Suspense } from "react"; // Import useState and useEffect
import styles from "./pastSessions.module.css";
import SessionCard from "./sessionCard/sessionCard";
import LoadingCard from "./loadingCard/loadingCard"; // Correct import for LoadingCard
import { getPastSessions } from "@/lib/pastSessions";

export default function PastSessionsGrid() {
  return (
    <div className={styles.frame}>
      <h2>Suggested Sessions</h2>
      <Suspense
        fallback={
          <div className={styles.grid}>
            {[0, 1, 2, 3, 4, 5].map((_, index) => {
              return <LoadingCard key={index}></LoadingCard>;
            })}
          </div>
        }
      >
        <PastSessionsAsync></PastSessionsAsync>
      </Suspense>
    </div>
  );
}

async function PastSessionsAsync() {
  const sessions = await getPastSessions();
  return (
    <div className={styles.grid}>
      {sessions.map((session, index) => {
        return <SessionCard key={index} session={session} />;
      })}
    </div>
  );
}
