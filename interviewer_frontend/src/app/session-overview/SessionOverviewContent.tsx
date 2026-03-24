import styles from "./page.module.css";
import Summary from "./summary";
import Video from "./video";
import Transcript from "./transcript";
import Skills from "./skills";
import Feedback from "./feedback";
import GradeGauge from "./gradeGauge";
import { Session } from "@/types/session";

export default function SessionOverviewContent({
  session,
}: {
  session: Session;
}) {
  return (
    <div className={styles.row}>
      {/* LEFT COLUMN */}
      <div className={styles.column}>
        <h1 className={styles.title}>Summary</h1>
        <Summary session={session} />

        <h1 className={styles.title}>Skills Breakdown</h1>
        <Skills session={session} />

        <h1 className={styles.title}>Feedback</h1>
        <Feedback session={session} />

        <h1 className={styles.title}>
          What's Your Greatest Strength?
        </h1>
        <GradeGauge session={session} />
      </div>

      {/* RIGHT COLUMN */}
      <div className={styles.column}>
        <h1 className={styles.title}>Video</h1>
        <Video url={session.videos[0]?.url ?? ""} />

        <h1 className={styles.title}>Transcript</h1>
        <Transcript text={session.transcript} />
      </div>
    </div>
  );
}