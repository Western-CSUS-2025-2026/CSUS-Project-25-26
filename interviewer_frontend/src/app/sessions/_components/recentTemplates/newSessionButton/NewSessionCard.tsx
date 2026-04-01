"use client";

import InvertedPlusIcon from "@/components/icons/invertedPlusIcon";
import styles from "./newSessionCard.module.css";
import { useRouter } from "next/navigation";

export default function NewSessionCard() {
  const router = useRouter();
  function openModal() {
    const params = new URLSearchParams(window.location.search);
    params.set("newSession", "1");
    params.set("step", "select");
    params.delete("templateId");

    router.push(`/sessions?${params.toString()}`);
  }

  return (
    <div
      className={styles.button}
      onClick={openModal}
      role="button"
      tabIndex={0}
    >
      <div className={styles.labelGroup}>
        <h3 className={styles.title}>New Session</h3>
        <p className={styles.subtitle}>
          Start a new session with a curated template
        </p>
      </div>

      <InvertedPlusIcon
        size="2.3em"
        foreground="var(--accent)"
        background="var(--accent-primary-text)"
      />
    </div>
  );
}
