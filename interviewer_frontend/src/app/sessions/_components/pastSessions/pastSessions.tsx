'use client'
import { useState, useEffect } from "react";  // Import useState and useEffect
import styles from "./pastSessions.module.css";
import SessionCard from "./sessionCard";
import LoadingCard from "./loadingCard";  // Correct import for LoadingCard
import type { SimpleSession } from "@/types/simpleSession";
import { getPastSessions } from "@/lib/pastSessions";

// ✅ client-side component with async data fetch
export default function PastSessionsGrid() {
  const [sessions, setSessions] = useState<SimpleSession[]>([]);  // State to store the sessions
  const [isLoading, setIsLoading] = useState(true);  // Track if we are loading data

  // Fetch sessions data
  useEffect(() => {
    const fetchData = async () => {
      const fetchedSessions = await getPastSessions(); // Fetch the sessions
      setSessions(fetchedSessions);  // Update state with the fetched data
      setIsLoading(false);  // Set loading to false when data is fetched
    };

    fetchData(); // Call the fetch function when component mounts
  }, []);  // Empty dependency array means this runs once when the component mounts

  return (
    <div className={styles.frame}>
      <h1 style={{ marginBottom: 0 }}>Past Sessions</h1>

      <div className={styles.grid}>
        {isLoading ? (
          // If we're still loading, show the skeleton card (LoadingCard)
          Array.from({ length: 5 }).map((_, index) => (
            <LoadingCard key={index} />
          ))
        ) : (
          // Once the data is fetched, show the actual session cards
          sessions.map((session, index) => (
            <SessionCard key={index} session={session} />
          ))
        )}
      </div>
    </div>
  );
}
