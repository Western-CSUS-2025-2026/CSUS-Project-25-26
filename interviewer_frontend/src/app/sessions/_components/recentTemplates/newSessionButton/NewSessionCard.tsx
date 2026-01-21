"use client";

import InvertedPlusIcon from "@/components/icons/invertedPlusIcon";
import styles from "./newSessionCard.module.css";

// Button to start a new session
export default function NewSessionCard() {
  return (
    <div
      className={styles.button}
      onClick={() => alert("New Session modal will open soon")}
    >
      {/* Left text section */}
      <div className={styles.labelGroup}>
        <h3 className={styles.title}>New Session</h3>
        <p className={styles.subtitle}>
          Start a new session with a curated template
        </p>
      </div>

      {/* Plus icon */}
      <InvertedPlusIcon
        size={"2.3em"}
        foreground="var(--accent)"
        background="var(--accent-primary-text)"
      ></InvertedPlusIcon>
    </div>
  );
}
