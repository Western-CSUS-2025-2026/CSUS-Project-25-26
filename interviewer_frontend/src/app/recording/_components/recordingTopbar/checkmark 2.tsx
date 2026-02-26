export default function CheckMark({
  size = 100,
  stroke = 100,
  color = "var(--accent-primary-text)"
}: {
  size?: number;
  height?: number;
  stroke?: number;
  color?: string;
}) {
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" fill="none">
      <line
        x1="40" y1="70"
        x2="24" y2="54"
        stroke={color}
        strokeWidth={stroke}
        strokeLinecap="round"
      />
      <line
        x1="40" y1="70"
        x2="76" y2="34"
        stroke={color}
        strokeWidth={stroke}
        strokeLinecap="round"
      />
    </svg>
  );
}
