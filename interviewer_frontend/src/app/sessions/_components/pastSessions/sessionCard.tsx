'use client';

import Card from "@/components/card/card";
import type { SimpleSession } from "@/types/simpleSession";
import "./module.css";
import { convertToLetterGrade } from "./gradeConvert";


interface SessionCardProps {
  session: SimpleSession; // now always passed from parent
}

export default function SessionCard({ session }: SessionCardProps) {
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

          {/* Processing message OR empty space */}
          <div className="ProccessingText">
            {session.state === "PROCESSING" ? (
              <p>This may take a few minutes...</p>
            ) : (
              <p>&nbsp;</p>   /* non-breaking space keeps layout consistent */
            )}
          </div>
          
          <div className = 'buttonBackground'>
            {session.state === "PROCESSING" ? (
              <p>Generating Report...</p>
            ) : (
              <p style = {{fontWeight:400}}>View Full Report</p>   /* non-breaking space keeps layout consistent */
            )}
          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div className="rightColumn">
          <div className="statusBox">
            <h3 style={{ color: "var(--secondary-text)" }}>{session.state}</h3>
          </div>
          <div className="dateBox">
            <h3 style={{ color: "var(--secondary-text)", fontWeight: 400 }}>
              {new Date(session.createTime).toLocaleDateString("en-US", {
                month: "2-digit",
                day: "2-digit",
                year: "2-digit",
              })}
            </h3>
          </div>


          {session.state === "COMPLETED" && (
          <div className="gauge">
            <div className="gauge-ring">
              <span className="gauge-segment gauge-segment-1" />
              <span className="gauge-segment gauge-segment-2" />
              <span className="gauge-segment gauge-segment-3" />
              <span className="gauge-segment gauge-segment-4" />
              <span className="gauge-segment gauge-segment-5" />
            </div>

            <h1 style={{ color: "var(--accent)" }}>
              {convertToLetterGrade(session.overallGrade.overallGrade)}
            </h1>
          </div>
        )}

      {session.state === "PROCESSING" && (
        <div className="loader"></div>
      )}
        </div>
      </div>
      
    </Card>
  );
  
}
