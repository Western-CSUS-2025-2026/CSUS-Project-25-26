import styles from "./questionsList.module.css";
import Card from "@/components/card/card";

interface QuestionsListProps {
  questions: string[];
}

export default function QuestionsList({ questions }: QuestionsListProps) {
  return (
    <Card>
      <div className={styles.questionsList}>
        <div className={styles.header}>
          <h2 className={styles.title}>Questions</h2>
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