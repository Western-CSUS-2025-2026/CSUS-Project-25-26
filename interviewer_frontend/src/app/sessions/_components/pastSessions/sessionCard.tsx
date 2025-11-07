import Card from "@/components/card/card";
import type { SimpleSession } from "@/types/simpleSession";
import {
  defaultCompletedSimpleSession,
} from "@/types/simpleSession";
import "./sessionCard.css";

interface SessionCardProps {
  session?: SimpleSession;
}

export default function SessionCard({
  session = defaultCompletedSimpleSession,
}: SessionCardProps) {
  return (
    <Card>
      <div className="cardContent">
        {/* LEFT COLUMN */}
        <div className="leftColumn">
          <div className="SessionBox">
            <h2>{session.title}</h2>
            <p>{session.template.title}</p>
            <p>{session.template.id}</p>
          </div>
          <div className="ProccessingText">
            <p>This may take a few minutes...</p>
          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div className="rightColumn">
          <div className="statusBox">
            <h3 style={{ color: "var(--secondary-text)" }}>{session.state}</h3>
          </div>
          <div className="dateBox">
            <h3 style={{ color: "var(--secondary-text)",fontWeight:400 }} >
              {new Date(session.createTime).toLocaleDateString("en-US", {
                month: "2-digit",
                day: "2-digit",
                year: "2-digit",
              })}
            </h3>
          </div>
        </div>
      </div>
    </Card>
  );
}
