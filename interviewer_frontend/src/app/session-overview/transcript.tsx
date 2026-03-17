import styles from "./transcript.module.css";
import Card from "@/components/card/card";

type TranscriptProps = {
  text: string;
};

export default function Transcript({ text }: TranscriptProps) {
  return (
    <Card>
      <div className={styles.transcriptBox}>
        <p>{text}</p>
      </div>
    </Card>
  );
}