"use client";

import styles from "./newSessionButton.module.css";

// Button to start a new session
export default function NewSessionButton() {
  return (
    <button
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
      <div className={styles.plusIcon}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
          <path
            d="M12 5v14m-7-7h14"
            stroke="var(--primary-text)"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
      </div>
    </button>
  );
}
