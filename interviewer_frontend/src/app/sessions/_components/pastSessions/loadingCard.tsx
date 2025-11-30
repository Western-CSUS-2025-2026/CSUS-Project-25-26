import Card from "@/components/card/card";
import styles from "./sessionCard.module.css";

export default function LoadingCard() {
  return (
    <Card>
      <div className={styles.cardContent}>

        {/* LEFT COLUMN */}
        <div className={styles.leftColumn}>
          <div className={styles.sessionBox}>
            <div className={styles.loading1}></div>
            <div className={styles.loading2}></div>
            <div className={styles.loading3}></div>
          </div>

          <div className={styles.loadingButton}></div>
        </div>

        {/* RIGHT COLUMN */}
        <div className={styles.rightColumn}>
          <div className={styles.statusBox}>
            <div className={styles.loading4}></div>
          </div>

          <div className={styles.dateBox}>
            <div className={styles.loading5}></div>
          </div>

          {/* Loading Gauge */}
          <div className={styles.gauge}>
            <div className={styles.gaugeRing}>
              <div className={`${styles.gaugeSegment} ${styles.gaugeSegment1}`}></div>
              <div className={`${styles.gaugeSegment} ${styles.gaugeSegment2}`}></div>
              <div className={`${styles.gaugeSegment} ${styles.gaugeSegment3}`}></div>
              <div className={`${styles.gaugeSegment} ${styles.gaugeSegment4}`}></div>
              <div className={`${styles.gaugeSegment} ${styles.gaugeSegment5}`}></div>
            </div>

            <div className={styles.loadingGrade}></div>
          </div>

        </div>

      </div>
    </Card>
  );
}
