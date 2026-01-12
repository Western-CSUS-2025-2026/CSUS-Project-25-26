import styles from "./transcript.module.css";

interface TranscriptProps {
  transcript: string;
}

export default function Transcript({ transcript }: TranscriptProps) {
  return (
    <div className={styles.transcriptSection}>
      <div className={styles.transcriptCard}>
        <p className={styles.transcriptText}>{transcript}</p>
      </div>
    </div>
  );
}