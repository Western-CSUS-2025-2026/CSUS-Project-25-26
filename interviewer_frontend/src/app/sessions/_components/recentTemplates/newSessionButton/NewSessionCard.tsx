"use client";

import InvertedPlusIcon from "@/components/icons/invertedPlusIcon";
import styles from "./newSessionCard.module.css";

export default function NewSessionCard() {
  function openModal() {
    const params = new URLSearchParams(window.location.search);
    params.set("newSession", "1");
    params.set("step", "select");
    params.delete("templateId");

    window.history.pushState({}, "", `/sessions?${params.toString()}`);

    // Force client components to react immediately
    window.dispatchEvent(new Event("urlchange"));
  }

  return (
    <div className={styles.button} onClick={openModal} role="button" tabIndex={0}>
      <div className={styles.labelGroup}>
        <h3 className={styles.title}>New Session</h3>
        <p className={styles.subtitle}>Start a new session with a curated template</p>
      </div>

      <InvertedPlusIcon
        size="2.3em"
        foreground="var(--accent)"
        background="var(--accent-primary-text)"
      />
    </div>
  );
}
