import LoadingSpinner from "@/components/loadingSpinner/loadingSpinner";
import styles from "./page.module.css";

export default function Loading() {
  return (
    <div className={styles.pageWrapper}>
      <div className={styles.loadingContainer}>
        <LoadingSpinner />
        <p className={styles.loadingText}>Loading session details...</p>
      </div>
    </div>
  );
}
