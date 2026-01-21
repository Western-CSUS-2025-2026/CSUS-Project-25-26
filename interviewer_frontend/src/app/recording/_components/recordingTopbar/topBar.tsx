"use client";

import { useEffect, useState } from "react";
import styles from "./topBar.module.css";
import CurrentQuestions from "./currentQuestion";
import QuestionStage from "./questionStage";
import RecordingBox from "./recordingBox";

export default function TopBar() {
  // Questions
  const [currentQuestion] = useState(3);
  const totalQuestions = 5;

  // Stage
  const [stage] = useState<"preparing" | "answering">("answering");

  // Recording state
  const [recording, setRecording] = useState(false);
  const [duration, setDuration] = useState(0);

  // duration logic 
  useEffect(() => {
    if (!recording) return;

    const t = setTimeout(() => {
      setDuration((d) => d + 1);
    }, 1000);

    return () => clearTimeout(t);
  }, [recording, duration]);

  return (
    <div className={styles.topBar}>
      <div className={styles.slot}>
        <CurrentQuestions
          current={currentQuestion}
          total={totalQuestions}
        />
      </div>

      <div className={styles.slot}>
        <QuestionStage stage={stage} />
      </div>

      <div className={styles.slot}>
        <RecordingBox
          recording={recording}
          duration={duration}
          onToggleRecording={() => setRecording((r) => !r)}
        />
      </div>
    </div>
  );
}
