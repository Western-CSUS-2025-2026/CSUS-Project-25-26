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

        <h1 className={styles.title}>Transcript</h1>
        <Transcript text={session.transcript} />

        {Array.from({ length: session.videos.length }, (_, index) => index).map(
          (i) => {
            return (
              <div key={i} style={{ width: "100%" }}>
                <h1 className={styles.title} style={{ marginBottom: "0.67em" }}>
                  {session.grades[i].question}
                </h1>
                <GradeGauge grade={session.grades[i]} />
                <Feedback feedback={session.grades[i].feedback} />
              </div>
            );
          },
        )}
      </div>

      {/* RIGHT COLUMN */}
      {/* <div className={styles.column}> */}
      {/*   <h1 className={styles.title}>Video</h1> */}
      {/*   <Video url={session.videos[0]?.url ?? ""} /> */}
      {/**/}
      {/*   <h1 className={styles.title}>Transcript</h1> */}
      {/*   <Transcript text={session.transcript} /> */}
      {/* </div> */}
    </div>
  );
}
