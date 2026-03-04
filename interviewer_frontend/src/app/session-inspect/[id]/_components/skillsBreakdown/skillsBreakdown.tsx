import { Score } from "@/types/session";
import styles from "./skillsBreakdown.module.css";

interface SkillsBreakdownProps {
  scores: Score[];
}

export default function SkillsBreakdown({ scores }: SkillsBreakdownProps) {
  return (
    <div className={styles.skillsCard}>
      <div className={styles.skillsGrid}>
        {scores.map((score, index) => (
          <div key={index} className={styles.skillItem}>
            <div className={styles.skillHeader}>
              <h3 className={styles.skillTitle}>{score.title}</h3>
              <p className={styles.skillDescription}>{score.description}</p>
            </div>

            <div className={styles.progressBar}>
              <div
                className={styles.progressFill}
                style={{ width: `${score.score * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}