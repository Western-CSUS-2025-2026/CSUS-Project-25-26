import styles from "./page.module.css";
import Summary from "./summary";
import Video from "./video";
import Transcript from "./transcript";
import { defaultSession } from "@/types/session"; 
import Skills from "./skills";
import Feedback from "./feedback";
import GradeGauge from "./gradeGauge";


export default function SessionOverview() {
  return (
    <div className={styles.container}>
      <div className={styles.row}>

        {/* LEFT COLUMN */}
        <div className={styles.column}>
          <h1 className={styles.title}>Summary</h1>
          <Summary />
          <h1 className={styles.title}>Skills Breakdown</h1>
          <Skills />
          <Feedback />
          <h1 className={styles.title}>What's Your Greatest Strength?</h1>
          <GradeGauge />
          <Feedback />
        </div>

        {/* RIGHT COLUMN */}
        <div className={styles.column}>
          <h1 className={styles.title}>Video</h1>

          <Video
            url={defaultSession.videos[0].url}
            question={defaultSession.videos[0].question}
          />
          <h1 className={styles.title}>Transcript</h1>
          <Transcript text={defaultSession.transcript} />
        </div>

      </div>
    </div>
  );
}