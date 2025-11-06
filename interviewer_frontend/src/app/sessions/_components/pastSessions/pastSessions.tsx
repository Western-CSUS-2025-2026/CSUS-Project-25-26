// use @lib/pastSesssion function to fetch past sessions
'use client';

import styles from "./pastSessions.module.css";
import SessionCard from "./sessionCard";

export default function PastSessionsGrid() {
  return (
    <div className={styles.frame}>
      <h1>Past Sessions</h1>

      <div className={styles.grid}>
        {Array.from({ length: 9 }).map((_, i) => (
          <SessionCard key={i} />
        ))}
      </div>
      
    </div>
  );
}
