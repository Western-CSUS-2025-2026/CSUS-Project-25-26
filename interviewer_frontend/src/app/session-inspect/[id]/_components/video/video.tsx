import styles from "./video.module.css";

interface VideoProps {
  videoUrl: string;
}

export default function Video({ videoUrl }: VideoProps) {
  return (
    <div className={styles.videoSection}>
      <div className={styles.videoCard}>
        <p className={styles.placeholder}>Video player placeholder</p>
        <p className={styles.url}>{videoUrl}</p>
      </div>
    </div>
  );
}