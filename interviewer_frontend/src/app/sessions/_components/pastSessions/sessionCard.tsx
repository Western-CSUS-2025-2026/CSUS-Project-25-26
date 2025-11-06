import Card from "@/components/card/card";
import type { SimpleSession } from "@/types/simpleSession";
import { defaultProcessingSimpleSession } from "@/types/simpleSession";
import "./sessionCard.css";

interface SessionCardProps {
  session?: SimpleSession;
}

export default function SessionCard({ session = defaultProcessingSimpleSession }: SessionCardProps) {
  return (
    <Card>
      <div className="cardContent">
        <div className="topRow">
          <div className="SessionNum">
            <h2>{session.title}</h2>
          </div>
          <div className="statusBox">
            <p>{session.state}</p>
          </div>
        </div>
        <div className="middleRow">
          <div className="dateBox">
            <p>
              {new Date(session.createTime).toLocaleDateString("en-US", {
                month: "2-digit",
                day: "2-digit",
                year: "2-digit",
              })}
            </p>
          </div>
        </div>
      </div>
    </Card>
  );
}
