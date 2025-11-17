"use client";

import { Template } from "@/types/template";
import styles from "./templateCard.module.css";

// Card for displaying a single recent template
export default function TemplateCard({ template }: { template: Template }) {
  return (
    <div className={styles.card}>
      {/* Text section */}
      <div>
        <h3 className={styles.title}>{template.title}</h3>
        <p className={styles.subtitle}>{template.description}</p>
      </div>

      {/* Plus icon button */}
      <div className={styles.plusIcon}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
          <path
            d="M12 5v14m-7-7h14"
            stroke="var(--accent-primary-text)"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
      </div>
    </div>
  );
}
