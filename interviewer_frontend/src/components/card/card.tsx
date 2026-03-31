interface CardProps {
  height?: string;
  width?: string;
  margin?: string;
  verticalMargin?: string;
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
    <>
      {/* cardStyle is located in global.css */}
      <div
        className="cardStyle"
        style={{
          height: props.fillHeight ? "100%" : props.height,
          width: props.fillWidth ? "100%" : props.width,
          margin: props.margin,
          marginTop: props.verticalMargin,
          marginBottom: props.verticalMargin,
        }}
      >
        {props.children}
      </div>
    </>
  );
}

export default Card;
