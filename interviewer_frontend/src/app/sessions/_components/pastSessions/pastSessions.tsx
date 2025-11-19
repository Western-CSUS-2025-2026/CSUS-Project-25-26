import styles from "./pastSessions.module.css";
import SessionCard from "./sessionCard";
import type { SimpleSession } from "@/types/simpleSession";
import { getPastSessions } from "@/lib/pastSessions";

// ✅ server component with async data fetch
export default async function PastSessionsGrid() {
  const sessions: SimpleSession[] = await getPastSessions();

  return (
    <div className={styles.frame}>
      <h1 style={{ marginBottom: 0 }}>Past Sessions</h1>

      <div className={styles.grid}>
        {sessions.map((session, index) => (
          <SessionCard key={index} session={session} />
        ))}
      </div>
    </div>
  );
}
