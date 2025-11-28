"use client";

import { Template } from "@/types/template";
import styles from "./templateCard.module.css";
import InvertedPlusIcon from "@/components/icons/invertedPlusIcon";

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
      <InvertedPlusIcon
        size="2.3em"
        foreground={"var(--foreground)"}
        background={"var(--accent)"}
      ></InvertedPlusIcon>
    </div>
  );
}
