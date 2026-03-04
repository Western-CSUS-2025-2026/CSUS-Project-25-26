import Card from "@/components/card/card";
import styles from "./questionsList.module.css";

interface QuestionsListProps {
  questions: string[];
}

export default function QuestionsList({ questions }: QuestionsListProps) {
  return (
    <Card>
      <div className={styles.questionsList}>
        <div className={styles.header}>
          <div className={styles.titleContainer}>
            <h2 className={styles.title}>Questions</h2>
            <div className={styles.plusIcon}>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path
                  d="M10 4V16M4 10H16"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </div>
          </div>
          <p className={styles.subtitle}>The questions you answered in order</p>
        </div>

        <ul className={styles.questionsListItems}>
          {questions.map((question, index) => (
            <li key={index} className={styles.questionItem}>
              {question}
            </li>
          ))}
        </ul>
      </div>
    </Card>
  );
}