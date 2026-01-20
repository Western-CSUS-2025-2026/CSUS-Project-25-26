"use client";

import styles from "./loadingTemplateCard.module.css";

export default function LoadingTemplateCard() {
  return (
    <div className={styles.card}>
      <div className={styles.textGroup}>
        <div className={styles.lineShort}></div>
        <div className={styles.lineLong}></div>
      </div>

      <div className={styles.plusIcon}></div>
    </div>
  );
}
