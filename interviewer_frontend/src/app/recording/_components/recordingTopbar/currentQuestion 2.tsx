import Card from "@/components/card/card";
import styles from "./currentQuestions.module.css";
import CheckMark from "./checkmark";

type CurrentQuestionsProps = {
  current: number; // current question (1-based)
  total: number; // total number of questions
};

export default function CurrentQuestions({
  current,
  total,
}: CurrentQuestionsProps) {
  return (
    <div>
      <h3 className={styles.boxTitle}>Questions</h3>

      <Card>
        <div className={styles.row}>
          {Array.from({ length: total }, (_, i) => {
            const questionNumber = i + 1;

            // DONE
            if (questionNumber < current) {
              return (
                <div key={questionNumber} className={styles.circleDone}>
                  <CheckMark size={28} stroke={15} />
                </div>
              );
            }

            // CURRENT
            if (questionNumber === current) {
              return (
                <div key={questionNumber} className={styles.circleCurrent}>
                  <h2 className={styles.questionNumCurrent}>
                    {questionNumber}
                  </h2>
                </div>
              );
            }

            // UPCOMING
            return (
              <div key={questionNumber} className={styles.circle}>
                <h2 className={styles.questionNum}>{questionNumber}</h2>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
