import styles from "./invertedPlusIcon.module.css";

interface InvertedPlusIconProps {
  foreground: string;
  background: string;
  size?: string;
}
function InvertedPlusIcon(props: InvertedPlusIconProps) {
  return (
    <div
      style={{
        width: props.size,
        height: props.size,
        backgroundColor: props.background,
        color: props.foreground,
      }}
      className={styles.plusIcon}
    >
      <svg width="70%" height="70%" viewBox="0 0 24 24" fill="none">
        <path
          d="M12 5v14m-7-7h14"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
}

export default InvertedPlusIcon;
