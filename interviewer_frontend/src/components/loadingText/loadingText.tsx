import styles from "./loadingText.module.css";
type Size = "H1" | "H2" | "H3" | "P";
interface LoadingTextProps {
  children?: React.ReactNode;
  loading?: boolean;
  presetHeight?: Size;
  customHeight?: string;
  width: string;
}

/** Creates a blurred outline of where text should be when loading is true, when loading is false, is displays the content
 */
function LoadingText(props: LoadingTextProps) {
  const height = (size: Size) => {
    switch (size) {
      case "H1":
        return "var(--h1-font-size)";
      case "H2":
        return "var(--h2-font-size)";
      case "H3":
        return "var(--h2-font-size)";
      case "P":
        return "var(--p-font-size)";
      default:
        return "var(--p-font-size)";
    }
  };
  return (
    <div className={styles.container} style={{ width: props.width }}>
      {props.loading ? (
        <div
          className={styles.loading}
          style={{
            marginTop: "0.67em",
            marginBottom: "0.67em",
            height: props.customHeight ?? height(props.presetHeight ?? "P"),
          }}
        ></div>
      ) : (
        <div className={styles.text}>{props.children}</div>
      )}
    </div>
  );
}

export default LoadingText;
