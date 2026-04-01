import styles from "./feedback.module.css";
import Card from "@/components/card/card";
import { Feedback as FeedbackType } from "@/types/session";
interface FeedbackProps {
  feedback: FeedbackType;
}

export default function Feedback(props: FeedbackProps) {
  return (
    <Card verticalMargin="2em" fillWidth>
      <div className={styles.feedbackCard}>
        <h2 className={styles.title}>Feedback</h2>

        <div>
          <h3>{props.feedback.point}</h3>

          <p>{props.feedback.feedback}</p>
        </div>
      </div>
    </Card>
  );
}
