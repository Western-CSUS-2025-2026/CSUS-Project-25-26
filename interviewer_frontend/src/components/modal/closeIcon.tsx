import styles from "./modal.module.css";

function CloseIcon(props: { onDismiss?: () => void }) {
  const dismissExists: boolean = props.onDismiss != undefined;
  const onDismiss = () => {
    if (dismissExists) props.onDismiss!();
  };
  const closeView = () => {
    return (
      <div className={styles.modalIcon} onClick={onDismiss}>
        <svg
          width="36"
          height="36"
          viewBox="0 0 36 36"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g clipPath="url(#clip0_136_5038)">
            <path
              d="M8.68342 26.361C9.08237 26.76 9.73794 26.7493 10.1262 26.361L17.3669 19.1204L24.6042 26.3577C24.9957 26.7492 25.6513 26.76 26.0503 26.361C26.4492 25.9621 26.4459 25.2991 26.0543 24.9076L18.817 17.6702L26.047 10.4403C26.4385 10.0487 26.4492 9.39315 26.0503 8.99421C25.6513 8.59525 24.985 8.59526 24.5935 8.9868L17.3635 16.2168L10.1335 8.98681C9.74531 8.59858 9.08237 8.59524 8.68342 8.99419C8.28447 9.39314 8.2952 10.0487 8.68343 10.4369L15.9134 17.6669L8.67271 24.9076C8.28448 25.2958 8.28447 25.9621 8.68342 26.361Z"
              fill="currentColor"
            />
          </g>
          <defs>
            <clipPath id="clip0_136_5038">
              <rect
                width="25"
                height="24.5756"
                fill="white"
                transform="translate(0 17.6776) rotate(-45)"
              />
            </clipPath>
          </defs>
        </svg>
      </div>
    );
  };
  return <> {dismissExists ? closeView() : undefined}</>;
}

export default CloseIcon;
