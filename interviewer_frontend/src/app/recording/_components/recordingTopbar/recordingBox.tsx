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

export interface RecordingBoxProps {
  recording?: boolean;
  duration?: number;
  onToggleRecording?: () => void;
}

export default function RecordingBox({
  recording,
  duration,
  onToggleRecording,
}: RecordingBoxProps) {
  // internal fallback state (unchanged behavior)
  const [internalRecording, setInternalRecording] = useState(false);
  const [internalDuration, setInternalDuration] = useState(0);
  const intervalRef = useRef<number | null>(null);

  // decide source of truth
  const isPlaying = recording ?? internalRecording;
  const elapsedSeconds = duration ?? internalDuration;

  useEffect(() => {
    if (!isPlaying) {
      if (intervalRef.current !== null) {
        window.clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      return;
    }

    if (intervalRef.current !== null) return;

    intervalRef.current = window.setInterval(() => {
      setInternalDuration((t) => t + 1);
    }, 1000);

    return () => {
      if (intervalRef.current !== null) {
        window.clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [isPlaying]);

  const toggleRecording = () => {
    if (onToggleRecording) {
      onToggleRecording();
    } else {
      setInternalRecording((p) => !p);
    }
  };

  return (
    <div>
      <h3 className={styles.boxTitle}>Recording</h3>

      <Card>
        <div className={styles.row}>
          <div className={styles.left}>
            <div className={styles.recordingRow}>
              <div
                className={`${styles.recordingIndicator} ${
                  isPlaying ? styles.recordingOn : styles.recordingOff
                }`}
              >
                <div className={styles.recordingDot} />
                <p className={styles.recText}>REC</p>
              </div>
              
              <p className={styles.timeText}>
                {formatTime(elapsedSeconds)}
              </p>
            </div>

            <div className={styles.waveform}>
              <MicWaveform enabled={isPlaying} />
            </div>
          </div>

          <button
            type="button"
            className={styles.circleButton}
            onClick={toggleRecording}
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
