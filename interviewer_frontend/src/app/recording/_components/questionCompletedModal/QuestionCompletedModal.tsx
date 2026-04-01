"use client";

import styles from "./questionCompletedModal.module.css";
import { Check } from "lucide-react";

type Props = {
  nextQuestion: number;
  onNext: () => void;
};

export default function QuestionCompletedModal({
  nextQuestion,
  onNext,
}: Props) {
  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>
        <div className={styles.iconCircle}>
          <Check size={32} />
        </div>

        <h1 className={styles.title}>Question Completed</h1>

        <p className={styles.subtitle}>Ready for Question {nextQuestion}?</p>

        <button className={styles.nextButton} onClick={onNext}>
          <span>Next Question (#{nextQuestion})</span>
        </button>
      </div>
    </div>
  );
}
