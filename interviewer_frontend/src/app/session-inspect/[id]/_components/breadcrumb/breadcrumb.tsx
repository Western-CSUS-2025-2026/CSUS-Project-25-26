import Link from "next/link";
import styles from "./breadcrumb.module.css";

interface BreadcrumbProps {
  sessionId: string;
}

export default function Breadcrumb({ sessionId }: BreadcrumbProps) {
  return (
    <div className={styles.breadcrumb}>
      <Link href="/sessions" className={styles.backButton}>
        ← Back
      </Link>
      <span className={styles.separator}>/</span>
      <Link href="/sessions" className={styles.link}>
        Sessions
      </Link>
      <span className={styles.separator}>/</span>
      <span className={styles.current}>Session {sessionId}</span>
    </div>
  );
}