"use client";
import styles from "./page.module.css";
import WebcamCard from "./_components/webcam/webcamCard";
import TopBar from "./_components/recordingTopbar/topBar";
import useSession from "@/lib/sessionLib/useSession";
import Modal from "@/components/modal/modal";
import RecordingSidebar from "./_components/recordingSidebar/recordingSidebar";
import CompletedModal from "./_components/completedModal/completedModal";

import { useRouter, useSearchParams } from "next/navigation";
import QuestionCompletedModal from "./_components/questionCompletedModal/QuestionCompletedModal";

function RecordingPage() {
  const router = useRouter();
  const params = useSearchParams();
  const session = useSession(Number(params.get("sessionId")) ?? -1);
  const router = useRouter();

  function returnToSessions() {
    router.push("/sessions");
  }

  const returnToSessions = () => {
    router.push("/sessions");
  };

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
        <RecordingSidebar
          timeEnded={session.continueModalUp || session.finishModalUp}
          stage={session.state}
          onStart={session.startSession}
          onEnd={() => {}}
          time={session.timerDisplay}
        ></RecordingSidebar>
      </div>
      {session.finishModalUp ? (
        <CompletedModal
          onClick={returnToSessions}
          videosUploaded={session.videosUploadedCount}
          />
      ) : undefined}

      {session.continueModalUp ? (
        <QuestionCompletedModal
          nextQuestion={session.currentQuestionNumber + 1}
          onNext={session.startNextQuestion}
        ></QuestionCompletedModal>
      ) : undefined}
    </div>
  );
}

export default RecordingPage;
