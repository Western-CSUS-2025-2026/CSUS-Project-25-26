import Card from "@/components/card/card";
import styles from "./gradeGauge.module.css";
import { defaultGrading } from "@/types/session";
import Gauge from "@/components/gauge/gauge";

export default function GradeGauge() {
  return (
    <div className={styles.row}> 
    <div className="gradeCardOverride">
      <style>{`
        .gradeCardOverride .cardStyle {
          background-color: #cb9fe6 !important;
        }

        /*INVERT GAUGE COLORS */
        .gradeCardOverride {
          --foreground: #cb9fe6;
          --accent: #39333B;     
        }
      `}</style>

      <Card>
            <div className={styles.gradeCard}>
            <h1>Grade</h1>
            <p className={styles.gradeSub}>
                An associated letter grade
            </p>

            <div className={styles.gaugeWrapper}>
                <Gauge score={defaultGrading.overallGrade}/>
            </div>
            </div>
      </Card>
      
    </div>
      <Card>
        <div className={styles.barCard}>
          <h1>Skills Breakdown</h1>
          <div className={styles.skillBarsRow}>
            {defaultGrading.scores.map((s, index) => (
              <div className={styles.skillBarItem} key={index}>
                <div className={styles.verticalBar}>
                  <div
                    className={styles.barFill}
                    style={{ height: `${s.score * 100}%` }}
                  />
                </div>
                <p className={styles.skillLabel}>{s.title}</p>
              </div>
            ))}
          </div>
        </div>
      </Card>
    </div>
  );
}