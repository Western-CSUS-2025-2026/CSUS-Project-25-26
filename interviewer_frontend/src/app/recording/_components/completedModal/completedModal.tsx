import Modal from "../../../../components/modal/modal";
import styles from "./completedModal.module.css";

interface CompletedModalProps {
  onClick: () => void;
  videosUploaded: number;
  totalVideos: number;
}

export default function CompletedModal(props: CompletedModalProps) {
  const onClick = () => {
    if (props.videosUploaded == props.totalVideos) {
      props.onClick();
    }
  };
  return (
    <Modal width="20em" height="20em" onDismiss={props.onClick}>
      <div className={styles.container}>
        <h3 className={styles.title}>Nice work!</h3>
        <p className={styles.message}>
          {"You've completed all the questions."}
        </p>
        <p className={styles.message}>
          Videos uploaded: {props.videosUploaded}
        </p>
        <p>
          {props.videosUploaded == props.totalVideos
            ? ""
            : "Waiting for uploads..."}
        </p>
        <button
          style={{
            opacity: props.videosUploaded == props.totalVideos ? 1.0 : 0.5,
            cursor:
              props.videosUploaded == props.totalVideos
                ? "pointer"
                : "progress",
          }}
          className={styles.okayButton}
          onClick={onClick}
        >
          Back to sessions
        </button>
      </div>
    </Modal>
  );
}
