import Modal from "../../../../components/modal/modal";
import styles from "./completedModal.module.css";

interface CompletedModalProps {
    onClick: () => void;
    videosUploaded: number;
}

export default function CompletedModal(props: CompletedModalProps) {
    return (
        <Modal width="20em" height="20em" onDismiss={props.onClick}>
            <div className={styles.container}>
                <h3 className={styles.title}>Nice work!</h3>
                <p className={styles.message}>You've completed all the questions.</p>
                <p className={styles.message}>Videos uploaded: {props.videosUploaded}</p>
                <button className={styles.okayButton} onClick={props.onClick}>Back to sessions</button>
            </div>
        </Modal>
    )
}