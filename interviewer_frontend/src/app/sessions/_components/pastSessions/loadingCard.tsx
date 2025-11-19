import Card from "@/components/card/card";
import "../sessionCard.css";

export default function SkeletonCard() {
  return (
    <Card>
      <div className="cardContent">
        <div className="leftColumn">
          <div className="SessionBox">
            <div className="pill pill-title" />
            <div className="pill pill-line" />
            <div className="pill pill-line short" />
          </div>
          <div className="ProccessingText">
            <div className="pill pill-helper" />
          </div>
        </div>
        <div className="rightColumn">
          <div className="pill pill-status" />
          <div className="pill pill-date" />
        </div>
      </div>
    </Card>
  );
}
