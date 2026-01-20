import styles from "./styledInput.module.css";

interface StyledInputProps {
  placeholder?: string;
  name?: string;
  autoComplete?: string;
  fontSize?: string;
  width?: string;
  title?: string;
  subtext?: string;
  subtextStyle?: "Error" | "Warning" | "Valid" | "Plain";
}

function StyledInput(props: StyledInputProps) {
  const subtextColor = () => {
    switch (props.subtextStyle) {
      case "Error":
        return "red";
      case "Warning":
        return "yellow";
      case "Valid":
        return "green";
      case "Plain":
        return "var(--secondary-text)";
    }
    return "green";
  };

  return (
    <div
      style={{ fontSize: props.fontSize, width: props.width }}
      className={styles.container}
    >
      <div className={styles.title}>{props.title}</div>

      <div className={styles.inputContainer}>
        <input
          className={styles.input}
          placeholder={props.placeholder}
          autoComplete={props.autoComplete}
        />
      </div>
      <div
        style={{
          color: subtextColor(),
        }}
        className={styles.subtext}
      >
        {props.subtext}
      </div>
    </div>
  );
}

export default StyledInput;
