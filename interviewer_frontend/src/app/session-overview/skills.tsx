import styles from "./skills.module.css";
import Card from "@/components/card/card";
import { Session } from "@/types/session";

export default function Skills({ session }: { session: Session }) {
  const grading = session.overallGrade;

  return (
    <div style={{ width: "100%" }}>
      <Card fillWidth>
        <div className={styles.skillsCard}>
          <div className={styles.skillsBreakdown}>
            {grading.scores.map((s, index) => (
              <div key={index} className={styles.skillItem}>
                <h2 className={styles.title}>{s.title}</h2>
                <p className={styles.description}>{s.description}</p>

                <div className={styles.barBackground}>
                  <div
                    className={styles.barFill}
                    style={{ width: `${s.score * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </Card>
    </div>
  );
}

