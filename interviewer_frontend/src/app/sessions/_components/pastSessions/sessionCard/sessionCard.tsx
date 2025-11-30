import Card from "@/components/card/card";
import type { SimpleSession } from "@/types/simpleSession";
import styles from "./sessionCard.module.css";
import Gauge from "../../../../../components/gauge/gauge";
import LoadingSpinner from "@/components/loadingSpinner/loadingSpinner";

interface SessionCardProps {
  session: SimpleSession;
}

export default function SessionCard({ session }: SessionCardProps) {
  const stateText = () => {
    if (session.state == "COMPLETED") {
      return "Completed";
    }
    return "Processing";
  };
  return (
    <Card>
      <div className={styles.cardContent}>
        {/* LEFT COLUMN */}
        <div className={styles.leftColumn}>
          <div className={styles.SessionBox}>
            <h2>{session.title}</h2>
            <p>{session.template.title}</p>
            <p>{session.template.id}</p>
          </div>

          <div className={styles.processingText}>
            {session.state === "PROCESSING" ? (
              <p>This may take a few minutes...</p>
            ) : (
              <p>&nbsp;</p>
            )}
          </div>

          <div className={styles.buttonBackground}>
            {session.state === "PROCESSING" ? (
              <p className={styles.buttonGenText}>Generating Report...</p>
            ) : (
              <p className={styles.buttonText}>View Full Report</p>
            )}
          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div className={styles.rightColumn}>
          <div className={styles.statusBox}>
            <h3 className={styles.statusText}>{stateText()}</h3>
          </div>

          <div className={styles.dateBox}>
            <h3 className={styles.dateText}>
              {new Date(session.createTime).toLocaleDateString("en-US", {
                month: "2-digit",
                day: "2-digit",
                year: "2-digit",
              })}
            </h3>
          </div>

          {session.state === "COMPLETED" && (
            <Gauge score={session.overallGrade.overallGrade} />
          )}

          {session.state === "PROCESSING" && <LoadingSpinner></LoadingSpinner>}
        </div>
      </div>
    </Card>
  );
}
