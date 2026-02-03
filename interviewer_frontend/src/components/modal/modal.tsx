import CloseIcon from "./closeIcon";
import styles from "./modal.module.css";

export interface ModalProps {
  children?: React.ReactNode;
  width?: string;
  height?: string;
  flexDirection?: "row" | "column";
  alignItems?: string;
  onDismiss?: () => void;
}

function Modal(props: ModalProps) {
  return (
    // modal container (darken background)
    <div className={styles.modalContainer}>
      {/* main content container */}
      <div
        style={{
          height: props.height,
          flexDirection: props.flexDirection,
          width: props.width,
          alignItems: props.alignItems,
        }}
        className={styles.modalContent + " cardStyle"}
      >
        {/* main content */}
        {props.children}
        {/* the close button */}
        <CloseIcon onDismiss={props.onDismiss}></CloseIcon>
      </div>
    </div>
  );
}

export default Modal;
