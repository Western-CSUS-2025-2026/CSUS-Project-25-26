import Card from "@/components/card/card";
import type { SimpleSession } from "@/types/simpleSession";
import styles from "./sessionCard.module.css";
import Gauge from "../../../../../components/gauge/gauge";
import LoadingSpinner from "@/components/loadingSpinner/loadingSpinner";
import Link from "next/link";
import XMark from "@/components/xmark/xmark";

interface SessionCardProps {
  session: SimpleSession;
}

export default function SessionCard({ session }: SessionCardProps) {
  const stateText = () => {
    if (session.state == "COMPLETED") {
      return "Completed";
    } else if (session.state == "INCOMPLETE") {
      return "Incomplete";
    }
    return "Processing";
  };

  const button = () => {
    switch (session.state) {
      case "PROCESSING": {
        return (
          <div className={styles.buttonBackground}>
            {" "}
            <p className={styles.buttonGenText}>Generating Report...</p>
          </div>
        );
      }

      case "INCOMPLETE": {
        return (
          <div className={styles.buttonBackground}>
            <p className={styles.buttonGenText}>Incomplete</p>
          </div>
        );
      }
      case "COMPLETED": {
        return (
          <Link
            href={`/session-inspect/${session.id}`}
            className={styles.buttonBackground}
          >
            <p className={styles.buttonText}>View Full Report</p>
          </Link>
        );
      }
    }
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

          <div className={styles.proccessingText}>
            {session.state === "PROCESSING" ? (
              <p className={styles.proccessingText}>
                This may take a few minutes...
              </p>
            ) : (
              <p>&nbsp;</p>
            )}
            {session.state === "INCOMPLETE" ? (
              <p className={styles.proccessingText}>
                All questions were not completed
              </p>
            ) : (
              <p>&nbsp;</p>
            )}
          </div>
          {button()}
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
            <Gauge score={session.overallGrade} />
          )}

          {session.state === "INCOMPLETE" && <XMark size="8em"></XMark>}
          {session.state === "PROCESSING" && <LoadingSpinner></LoadingSpinner>}
        </div>
      </div>
    </Card>
  );
}
