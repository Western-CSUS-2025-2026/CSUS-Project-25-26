import styles from "./gauge.module.css";

interface GaugeProps {
  score: number; // 0.0–1.0
}

/* Convert numeric score to letter grade */
function convertToLetterGrade(score: number): string {
  if (score >= 0.9333) return "A+";
  if (score >= 0.8667) return "A";
  if (score >= 0.8) return "A-";
  if (score >= 0.7333) return "B+";
  if (score >= 0.6667) return "B";
  if (score >= 0.6) return "B-";
  if (score >= 0.5333) return "C+";
  if (score >= 0.4667) return "C";
  if (score >= 0.4) return "C-";
  if (score >= 0.3333) return "D+";
  if (score >= 0.2667) return "D";
  if (score >= 0.2) return "D-";
  if (score >= 0.1333) return "F+";
  if (score >= 0.0667) return "F";
  return "F-";
}

/** snap a 0–1 value to 0, 1/3, 2/3, or 1 */
function snapFill(value: number): number {
  const STEPS = [0, 1 / 3, 2 / 3, 1];
  let closest = STEPS[0];
  let minDiff = Math.abs(value - closest);

  for (const step of STEPS) {
    const diff = Math.abs(value - step);
    if (diff < minDiff) {
      minDiff = diff;
      closest = step;
    }
  }

  return closest;
}

export default function Gauge({ score }: GaugeProps) {
  const clamped = Math.max(0, Math.min(1, score)); // Clamp between 0 and 1
  const letter = convertToLetterGrade(clamped);

  const NUM_SEGMENTS = 5;
  const segmentSize = 1 / NUM_SEGMENTS;

  const fills = Array.from({ length: NUM_SEGMENTS }, (_, i) => {
    const start = i * segmentSize;
    const end = start + segmentSize;

    let rawFill: number;
    if (clamped >= end)
      rawFill = 1; // fully filled
    else if (clamped <= start)
      rawFill = 0; // empty
    else rawFill = (clamped - start) / segmentSize; // partial 0–1

    return snapFill(rawFill);
  });

  // Special case: exactly 0.5 → 2 full, 3rd half
  if (clamped === 0.5) {
    fills[0] = 1;
    fills[1] = 1;
    fills[2] = 0.5;
    fills[3] = 0;
    fills[4] = 0;
  }

  return (
    <div className={styles.gauge}>
      <div className={styles.gaugeRing}>
        {fills.map((fill, index) => {
          // .gaugeSegment-1, .gaugeSegment-2, ... in CSS
          const positionClass = styles[`gaugeSegment-${index + 1}`];

          return (
            <div key={index}>
              {/* Ghost/background segment */}
              <span
                className={`${styles.gaugeSegmentGhost} ${positionClass}`}
              />

              {/* Filled segment */}
              <span className={`${styles.gaugeSegmentFill} ${positionClass}`}>
                <div
                  className={styles.gaugeFill}
                  style={{ width: `${fill * 100}%` }}
                />
              </span>
            </div>
          );
        })}
      </div>

      <h1 className={styles.gaugeLetter}>{letter}</h1>
    </div>
  );
}
