import style from "./card.module.css";

interface CardProps {
  height?: string;
  width?: string;
  margin?: string;
  children?: React.ReactNode;
  fillWidth?: boolean;
  fillHeight?: boolean;
}
/**
 * Used as a base for any card
 *
 */
function Card(props: CardProps) {
  return (
    <div
      className={style.card}
      style={{
        height: props.fillHeight ? "calc(100% - 2em)" : props.height,
        width: props.fillWidth ? "calc(100% - 2em)" : props.width,
        margin: props.margin,
      }}
    >
      {props.children}
    </div>
  );
}

export default Card;
