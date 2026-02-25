
import Card from "@components/card/card.tsx";
import { useState, useEffect } from "react";
import styles from "./recordingSidebar.module.css";

type Stage = "preparing" | "answering";

export default function RecordingSidebar() {
  const [stage, setStage] = useState<Stage>("preparing");
  const [timeRemaining, setTimeRemaining] = useState(30);
  const [timeEnded, setTimeEnded] = useState(false);

  let totalTime;
  if (stage === "answering") {
    totalTime = 120;
  } else {
    totalTime = 30;
  }
  const minutes = Math.floor(timeRemaining / 60);
  const seconds = timeRemaining % 60;

  useEffect(() => {
    if (timeEnded) {
      return;
    }

    if (timeRemaining <= 0) {
      if (stage === "preparing") {
        setStage("answering");
        setTimeRemaining(120);
      }
      else if (stage === "answering") {
        setTimeEnded(true);
      }
      return;
    }

    const timer = setInterval(() => {
      setTimeRemaining(prev => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeRemaining, stage, timeEnded]);

  const progress = timeRemaining / totalTime;
  const radius = 120;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference * (1 - progress);

  let stageText;
  if (stage === "preparing") {
    stageText = "Preparing";
  }
  else {
    stageText = "Answering";
  }

  return (
    <Card fillHeight fillWidth>
      <div className={styles.container}>
        <div className={styles.header}>
          <h1>{stageText}</h1>
        </div>

        <div className={styles.timerWrapper}>
          <svg width="300" height="300" className={styles.svg}>
            <circle
              cx="150"
              cy="150"
              r={radius}
              stroke="var(--border)"
              strokeWidth="20"
              fill="none"
            />
            <circle
              cx="150"
              cy="150"
              r={radius}
              stroke="var(--accent)"
              strokeWidth="20"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              style={{ transition: "stroke-dashoffset 1s linear" }}
            />
          </svg>

          <div className={styles.timerCenter}>
            <div className={styles.time}>
              {minutes}:{seconds.toString().padStart(2, "0")}
            </div>
            <p className={styles.remaining}>Remaining</p>
          </div>
        </div>

        <div className={styles.footer}>
          {!timeEnded && stage === "preparing" && (
            <button
              className={styles.primaryButton}
              onClick={() => {
                setStage("answering");
                setTimeRemaining(120);
              }}
            >
              Start
            </button>
          )}

          {!timeEnded && stage === "answering" && (
            <>
              <button
                className={styles.endButton}
                onClick={() => setTimeEnded(true)}
              >
                End Question
              </button>
              <p className={styles.warning}>
                You cannot continue later after ending this question.
              </p>
            </>
          )}

          {timeEnded && (
            <p className={styles.endedText}>Question ended</p>
          )}
        </div>
      </div>
    </Card>
  );
}
