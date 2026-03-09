"use client";

import { useState } from "react";
import Card from "@/components/card/card";
import styles from "./page.module.css";
import QuestionCompletedModal from "../_components/questionCompletedModal/QuestionCompletedModal";

function SessionOverview() {

  const [currentQuestion, setCurrentQuestion] = useState(1);
  const [showCompletedModal, setShowCompletedModal] = useState(false);

  function handleNextQuestion() {
    setCurrentQuestion((q) => q + 1);
    setShowCompletedModal(false);
  }

  return (
    <div className={styles.container}>

      {/* TEMP button to simulate question completion */}
      <button
        onClick={() => setShowCompletedModal(true)}
        style={{ position: "absolute", top: 20, left: 20 }}
      >
        Simulate Complete
      </button>

      <div className={styles.leftColumn}>
        <div className={styles.topContainer}>
          {/* Question content will go here */}
        </div>
      </div>

      <div className={styles.rightColumn}>
        <h1>Recording</h1>
        <Card height="10em"></Card>

        <h1>Transcript</h1>
        <Card height="15em"></Card>
      </div>

      {showCompletedModal && (
        <QuestionCompletedModal
          nextQuestion={currentQuestion + 1}
          onNext={handleNextQuestion}
        />
      )}
    </div>
  );
}

export default SessionOverview;