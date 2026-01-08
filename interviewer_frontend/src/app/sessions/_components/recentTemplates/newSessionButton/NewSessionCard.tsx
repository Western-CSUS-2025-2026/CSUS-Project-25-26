"use client";

import { useRouter } from "next/navigation";
import InvertedPlusIcon from "@/components/icons/invertedPlusIcon";
import styles from "./newSessionCard.module.css";

// Button to start a new session
export default function NewSessionCard() {
  const router = useRouter();

  return (
    <div
      className={styles.button}
      onClick={() => {
        router.push("/sessions?newSession=1&step=select");
      }}
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
      />
    </div>
  );
}
