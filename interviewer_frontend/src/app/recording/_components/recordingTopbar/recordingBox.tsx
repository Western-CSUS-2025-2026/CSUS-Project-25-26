"use client";

import Card from "@/components/card/card";
import styles from "./recordingBox.module.css";
import MicWaveform from "./MicWaveform";

function formatTime(totalSeconds: number) {
  const m = Math.floor(totalSeconds / 60);
  const s = Math.floor(totalSeconds % 60);
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export interface RecordingBoxProps {
  canPause: boolean;
  recording: boolean;
  duration: number;
  onToggleRecording: () => void;
}

export default function RecordingBox({
  recording,
  duration,
  onToggleRecording,
  canPause,
}: RecordingBoxProps) {
  const isPlaying = recording;

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

              <p className={styles.timeText}>{formatTime(duration)}</p>
            </div>

            <div className={styles.waveform}>
              <MicWaveform enabled={isPlaying} />
            </div>
          </div>

          <button
            type="button"
            className={styles.circleButton}
            onClick={onToggleRecording}
            style={{ opacity: canPause ? 1 : 0.4 }}
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
