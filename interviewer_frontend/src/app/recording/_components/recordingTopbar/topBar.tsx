"use client";

import styles from "./topBar.module.css";
import CurrentQuestions from "./currentQuestion";
import QuestionStage from "./questionStage";
import RecordingBox from "./recordingBox";
import { SessionState } from "@/lib/sessionLib/useSession";

interface TopBarProps {
  currentQuestion: number;
  totalQuestions: number;
  isRecording: boolean;
  duration: number;
  pauseRecording: () => void;
  stage: SessionState;
}

export default function TopBar(props: TopBarProps) {
  return (
    <div className={styles.topBar}>
      <div className={styles.slot}>
        <CurrentQuestions
          current={props.currentQuestion}
          total={props.totalQuestions}
        />
      </div>

      <div className={styles.slot}>
        <QuestionStage stage={props.stage} />
      </div>

      <div className={styles.slot}>
        <RecordingBox
          canPause={props.stage == "Recording"}
          recording={props.isRecording}
          duration={props.duration}
          onToggleRecording={props.pauseRecording}
        />
      </div>
    </div>
  );
}
