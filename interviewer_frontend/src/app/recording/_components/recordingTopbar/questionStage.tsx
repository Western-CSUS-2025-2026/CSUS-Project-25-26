import Card from "@/components/card/card";
import styles from "./questionStage.module.css";

type Stage = "preparing" | "answering";

type QuestionStageProps = {
  stage: Stage;
};

export default function QuestionStage({ stage }: QuestionStageProps) {
  const isPreparing = stage === "preparing";
  const isAnswering = stage === "answering";

  return (
    <div>
      <h3 className={styles.boxTitle}>Stage</h3>

      <Card>
        <div className={styles.row}>
          {/* Preparing */}
          <div
            className={isPreparing ? styles.stageBoxActive : styles.stageBox}
          >
            <p className={isPreparing ? styles.activeText : styles.inactiveText}>
              Preparing
            </p>
          </div>

          {/* Answering */}
          <div
            className={isAnswering ? styles.stageBoxActive : styles.stageBox}
          >
            <p className={isAnswering ? styles.activeText : styles.inactiveText}>
              Answering
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
