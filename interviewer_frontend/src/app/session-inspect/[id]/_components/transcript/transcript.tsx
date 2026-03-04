import Card from "@/components/card/card";
import styles from "./transcript.module.css";

interface TranscriptProps {
  transcript: string;
}

export default function Transcript({ transcript }: TranscriptProps) {
  return (
    <Card width="100%">
      <div className={styles.transcriptSection}>
        <div className={styles.transcriptCard}>
          <p className={styles.transcriptText}>{transcript}</p>
        </div>
      </div>
    </Card>
  );
}