import Gauge from "@/components/gauge/gauge";
import styles from "./gradeCard.module.css";

interface GradeCardProps {
  score: number; // 0-1 value
}

export default function GradeCard({ score }: GradeCardProps) {
  return (
    <div className={styles.gradeCard}>
      <div className={styles.header}>
        <h2 className={styles.title}>Grade</h2>
        <p className={styles.subtitle}>An associated letter grade</p>
      </div>
      <div className={styles.gaugeContainer}>
        <Gauge score={score} />
      </div>
    </div>
  );
}