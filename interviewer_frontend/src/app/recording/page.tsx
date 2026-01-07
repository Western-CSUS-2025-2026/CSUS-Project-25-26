"use client";
import Card from "@/components/card/card";
import WebcamCard from "./_components/webcam/webcamCard";
import { useRecording } from "@/lib/useRecording";

function RecordingPage() {
  const rec = useRecording();
  return (
    <div style={{ display: "flex", flexDirection: "row", gap: "1em" }}>
      <WebcamCard webRef={rec.webRef}></WebcamCard>
      <Card width="20em">
        <button onClick={rec.startRecording}>Start</button>
        <button onClick={rec.endRecording}>End</button>
        <button onClick={rec.download}>Download</button>
        <div style={{ color: "green" }}>
          {rec.capturing ? "Capturing" : "Not"}
        </div>
      </Card>
    </div>
  );
}

export default RecordingPage;
