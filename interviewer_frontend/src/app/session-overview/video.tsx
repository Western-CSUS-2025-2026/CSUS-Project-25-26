import styles from "./video.module.css";

type VideoProps = {
  url: string;
};

export default function Video({ url }: VideoProps) {
  return (
    <div className={styles.videoCard}>
      <video className={styles.video} controls>
        <source src={url} type="video/mp4" />
      </video>
    </div>
  );
}
