import styles from "./video.module.css";

type VideoProps = {
  url: string;
  question: string;
};

export default function Video({ url, question }: VideoProps) {
  return (
    <div className={styles.videoCard}>
      <video className={styles.video} controls>
        <source src={url} type="video/mp4" />
      </video>
    </div>
  );
}