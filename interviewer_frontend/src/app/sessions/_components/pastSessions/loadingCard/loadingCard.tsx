import Card from "@/components/card/card";
import styles from "../sessionCard/sessionCard.module.css";
import loadingStyles from "./loadingCard.module.css";

export default function LoadingCard() {
  return (
    <Card>
      <div className={styles.cardContent}>
        {/* LEFT COLUMN */}
        <div className={styles.leftColumn}>
          <div className={styles.sessionBox}>
            <div className={loadingStyles.loading1}></div>
            <div className={loadingStyles.loading2}></div>
            <div className={loadingStyles.loading3}></div>
          </div>

          <div className={loadingStyles.loadingButton}></div>
        </div>

        {/* RIGHT COLUMN */}
        <div className={styles.rightColumn}>
          <div className={styles.statusBox}>
            <div className={loadingStyles.loading4}></div>
          </div>

          <div className={styles.dateBox}>
            <div className={loadingStyles.loading5}></div>
          </div>

          {/* Loading Gauge */}
          <div className={loadingStyles.gauge}>
            <div className={loadingStyles.gaugeRing}>
              <div
                className={`${loadingStyles.gaugeSegment} ${loadingStyles.gaugeSegment1}`}
              ></div>
              <div
                className={`${loadingStyles.gaugeSegment} ${loadingStyles.gaugeSegment2}`}
              ></div>
              <div
                className={`${loadingStyles.gaugeSegment} ${loadingStyles.gaugeSegment3}`}
              ></div>
              <div
                className={`${loadingStyles.gaugeSegment} ${loadingStyles.gaugeSegment4}`}
              ></div>
              <div
                className={`${loadingStyles.gaugeSegment} ${loadingStyles.gaugeSegment5}`}
              ></div>
            </div>

            <div className={loadingStyles.loadingGrade}></div>
          </div>
        </div>
      </div>
    </Card>
  );
}
