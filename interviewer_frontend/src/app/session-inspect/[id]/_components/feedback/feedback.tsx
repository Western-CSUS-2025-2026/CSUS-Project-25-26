import styles from "./feedback.module.css";
import { Feedback as FeedbackType } from "@/types/session";

interface FeedbackProps {
  feedback: FeedbackType[];
}

export default function Feedback({ feedback }: FeedbackProps) {
  return (
    <div className={styles.feedbackCard}>
      <div className={styles.header}>
        <p className={styles.subtitle}>Your next steps for improving your skills</p>
      </div>

      <div className={styles.feedbackList}>
        {feedback.map((item, index) => (
          <div key={index} className={styles.feedbackItem}>
            <h3 className={styles.feedbackPoint}>{item.point}</h3>
            <ul className={styles.suggestions}>
              {item.feedback.map((suggestion, idx) => (
                <li key={idx} className={styles.suggestion}>
                  {suggestion}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}