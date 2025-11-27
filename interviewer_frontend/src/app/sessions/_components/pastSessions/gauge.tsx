"use client";

import "./gauge.css";

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
  const clamped = Math.max(0, Math.min(1, score)); // Clamp the score between 0 and 1
  const letter = convertToLetterGrade(clamped);    // Convert score to letter grade

  const NUM_SEGMENTS = 5;  // Total of 5 segments
  const segmentSize = 1 / NUM_SEGMENTS;

  // Calculate how much fill should go into each segment
  const fills = Array.from({ length: NUM_SEGMENTS }, (_, i) => {
    const start = i * segmentSize;
    const end = start + segmentSize;

    let rawFill: number;
    if (clamped >= end) rawFill = 1;              // this segment fully filled
    else if (clamped <= start) rawFill = 0;       // this segment empty
    else rawFill = (clamped - start) / segmentSize; // partial [0,1]

    return snapFill(rawFill);  // Snap fill to 0, 1/3, 2/3, or 1
  });

  // If score is exactly 0.5, manually set it so 2 segments are filled and 3rd is half-filled
  if (clamped === 0.5) {
    fills[0] = 1;
    fills[1] = 1;
    fills[2] = 0.5;
    fills[3] = 0;
    fills[4] = 0;
  }

  return (
    <div className="gauge">
      <div className="gauge-ring">
        {fills.map((fill, index) => {
          const segClass = `gauge-segment-${index + 1}`;

          return (
            <div key={index}>
              {/* Ghost segment (dimmed at 30% opacity) */}
              <span
                className={`gauge-segment ${segClass} gauge-segment--ghost`}
              />

              {/* Filled segment (overlaid on ghost) */}
              <span
                className={`gauge-segment ${segClass} gauge-segment--fill`}
              >
                <div
                  className="gauge-fill"
                  style={{ width: `${fill * 100}%` }} // Dynamically adjust fill
                />
              </span>
            </div>
          );
        })}
      </div>

      <h1 className="gauge-letter">{letter}</h1>
    </div>
  );
}
