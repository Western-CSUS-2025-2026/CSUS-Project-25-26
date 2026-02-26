import { SessionState } from "@/lib/sessionLib/useSession";
import Card from "../../../../components/card/card";
import styles from "./recordingSidebar.module.css";

interface RecordingSidebarProps {
  stage: SessionState;
  time: number;
  timeEnded: boolean;
  onStart: () => void;
  onEnd: () => void;
}

export default function RecordingSidebar(props: RecordingSidebarProps) {
  const timeEnded = props.timeEnded;
  const stage = props.stage;
  let totalTime: number;
  if (stage == "Recording") {
    totalTime = 7;
  } else {
    totalTime = 5;
  }
  let timeRemaining = totalTime - props.time;
  if (props.timeEnded == true) {
    timeRemaining = 1;
    totalTime = 1;
  }

  const minutes = Math.floor(timeRemaining / 60);
  const seconds = Math.floor(timeRemaining % 60);

  const progress = timeRemaining / totalTime;
  const radius = 120;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference * (1 - progress);

  let stageText: string;
  if (stage === "Preparing") {
    stageText = "Preparing";
  } else {
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
              style={{ transition: "stroke-dashoffset 0.35s linear" }}
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
          {!timeEnded && stage === "Preparing" && (
            <button className={styles.primaryButton} onClick={props.onStart}>
              Start
            </button>
          )}

          {!timeEnded && stage === "Recording" && (
            <>
              <button className={styles.endButton} onClick={props.onEnd}>
                End Question
              </button>
              <p className={styles.warning}>
                You cannot continue later after ending this question.
              </p>
            </>
          )}

          {timeEnded && <p className={styles.endedText}>Question ended</p>}
        </div>
      </div>
    </Card>
  );
}
