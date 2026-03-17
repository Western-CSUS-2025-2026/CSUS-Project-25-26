import styles from "./skills.module.css";
import Card from "@/components/card/card";
import { defaultGrading} from "@/types/session";

export default function Skills() {
  return (
    <Card>
      <div className={styles.skillsCard}>
        <div className={styles.skillsBreakdown}>
          {defaultGrading.scores.map((s, index) => (
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
  );
}