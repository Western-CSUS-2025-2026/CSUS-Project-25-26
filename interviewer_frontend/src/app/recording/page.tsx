"use client";
import styles from "./page.module.css";
import WebcamCard from "./_components/webcam/webcamCard";
import TopBar from "./_components/recordingTopbar/topBar";
import useSession from "@/lib/sessionLib/useSession";
import Card from "@/components/card/card";
import Modal from "@/components/modal/modal";
import { useSearchParams } from "next/navigation";

function RecordingPage() {
  const params = useSearchParams();
  const session = useSession(Number(params.get("templateId")) ?? -1);

  return (
    <div style={{ gap: "1em", display: "flex", flexDirection: "column" }}>
      <h1 className={styles.questionTitle}>{session.currentQuestion}</h1>

      <TopBar
        currentQuestion={session.currentQuestionNumber + 1}
        totalQuestions={session.totalQuestions}
        isRecording={session.isRecording}
        duration={session.recordingDuration}
        stage={session.state}
        pauseRecording={session.toggleRecording}
      ></TopBar>
      <div style={{ display: "flex", flexDirection: "row", gap: "1em" }}>
        <WebcamCard webRef={session.webcam}></WebcamCard>
        <Card>
          <button onClick={session.startSession} style={{ color: "black" }}>
            Start Recording
          </button>
          <div style={{ color: "green" }}>{session.state}</div>
          <div style={{ color: "green" }}>{session.timerDisplay}</div>
        </Card>
      </div>
      {session.finishModalUp ? (
        <Modal width="20em" height="20em">
          <div>finished</div>
          <div>{"Videos uploaded: " + session.videosUploadedCount}</div>
        </Modal>
      ) : undefined}

      {session.continueModalUp ? (
        <Modal width="20em" height="20em" onDismiss={session.startNextQuestion}>
          <div>Completed question</div>
          <button onClick={session.startNextQuestion}>continue</button>
        </Modal>
      ) : undefined}
    </div>
  );
}

export default RecordingPage;
