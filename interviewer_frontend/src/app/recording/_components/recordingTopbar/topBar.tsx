// recording/_components/recordingTopbar/topBar.tsx
import styles from "./topBar.module.css";
import CurrentQuestions from "./currentQuestion";
import QuestionStage from "./questionStage";
import RecordingBox from "./recordingBox";

export default function TopBar() {
  return (
    <div className={styles.topBar}>
      <div className={styles.slot}>
        <CurrentQuestions current={3} total={5} />
      </div>

      <div className={styles.slot}>
        <QuestionStage stage="answering" />  
      </div>

      <div className={styles.slot}>
        <RecordingBox />
      </div>
    </div>
  );
}
