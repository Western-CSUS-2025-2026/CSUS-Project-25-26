import styles from "./feedback.module.css";
import Card from "@/components/card/card";
import { defaultGrading } from "@/types/session";

export default function Feedback() {
  return (
    <Card>
      <div className={styles.feedbackCard}>
        <h2 className={styles.title}>Feedback</h2>
        <p className={styles.description}>Your next steps for improving your skills</p>

        {defaultGrading.feedback.map((f, index) => (
          <div key={index}>
            <h3 className={styles.feedbackPoint}>{f.point}</h3>

            {f.feedback.map((tip, i) => (
              <p key={i}>{tip}</p>
            ))}
          </div>
        ))}
      </div>
    </Card>
  );
}