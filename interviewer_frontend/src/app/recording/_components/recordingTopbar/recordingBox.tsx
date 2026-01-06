"use client";

import { useEffect, useRef, useState } from "react";
import Card from "@/components/card/card";
import styles from "./recordingBox.module.css";
import MicWaveform from "./MicWaveform";

function formatTime(totalSeconds: number) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export default function RecordingBox() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    if (isPlaying) {
      if (intervalRef.current !== null) return;

      intervalRef.current = window.setInterval(() => {
        setElapsedSeconds((t) => t + 1);
      }, 1000);
    } else {
      if (intervalRef.current !== null) {
        window.clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }

    return () => {
      if (intervalRef.current !== null) {
        window.clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [isPlaying]);

  return (
        <div>
          <h3 className={styles.boxTitle}>Recording</h3>

          <Card>
      <div className={styles.row}>
        <div className={styles.left}>
          <div className={styles.recordingRow}>
            {isPlaying && (
              <div className={styles.recordingIndicator}>
                <div className={styles.recordingDot}></div>
                <p className={styles.recText}>REC</p>
              </div>
            )}
          <p className={styles.timeText}>{formatTime(elapsedSeconds)}</p>
          </div>

         <div className={styles.waveform}> <MicWaveform enabled={isPlaying} /> </div>

        </div>

        <button
          type="button"
          className={styles.circleButton}
          onClick={() => setIsPlaying((p) => !p)}
          aria-label={isPlaying ? "Pause timer" : "Start timer"}
        >
          {isPlaying ? (
            <div className={styles.pause}>
              <span />
              <span />
            </div>
          ) : (
            <div className={styles.play} />
          )}
        </button>
      </div>
    </Card>
    </div>
  );
}
