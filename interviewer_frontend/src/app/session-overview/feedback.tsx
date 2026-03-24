import styles from "./feedback.module.css";
import Card from "@/components/card/card";
import { Session } from "@/types/session";

export default function Feedback({ session }: { session: Session }) {
  const feedback = session.overallGrade.feedback ?? [];

  return (
    <Card>
      <div className={styles.feedbackCard}>
        <h2 className={styles.title}>Feedback</h2>

        {feedback.map((f, index) => {
          const tips = Array.isArray(f.feedback)
            ? f.feedback
            : f.feedback
            ? [f.feedback]
            : [];

          return (
            <div key={index}>
              <h3>{f.point}</h3>

              {tips.map((tip, i) => (
                <p key={i}>{tip}</p>
              ))}
            </div>
          );
        })}
      </div>
    </Card>
  );
}