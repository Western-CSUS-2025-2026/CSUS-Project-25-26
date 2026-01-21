import { RefObject, useEffect, useState } from "react";
import { useRecording } from "./useRecording";
import Webcam from "react-webcam";
import { useTimer } from "./useTimer";
import { getSessionInfo } from "../getSessionInfo";
import { sendRecording } from "./sendRecording";

export type SessionState = "Recording" | "Preparing";

interface UseSessionReturn {
  webcam: RefObject<Webcam | null>;
  toggleRecording: () => void;
  recordingDuration: number;
  timerDisplay: number;
  currentQuestion: string;
  currentQuestionNumber: number;
  isInitalLoading: boolean;
  state: SessionState;
  hasStarted: boolean;
  totalQuestions: number;
  isRecording: boolean;
  startSession: () => void;
  videosUploadedCount: number;
  continueModalUp: boolean;
  finishModalUp: boolean;
  startNextQuestion: () => void;
}

function useSession(): UseSessionReturn {
  const prepPhaseDurtion = 5000;
  const recordingPhaseDuration = 7000;
  const recording = useRecording();
  const [questionList, setQuestionList] = useState<string[]>([]);
  const [questionNum, setQuestionNum] = useState(0);
  const [videosUploaded, setVideosUploaded] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState("Start and questions will appear here...");
  const timer = useTimer();

  const [finishModalUp, setFinishModalUp] = useState(false);
  const [continueModalUp, setContinueModalUp] = useState(false);

  const [isLoading, setIsLoading] = useState(true);
  const [state, setState] = useState<SessionState>("Preparing");
  const [hasStarted, setHasStarted] = useState(false);

  useEffect(() => {
    setIsLoading(true);
    getSessionInfo().then((info) => {
      setQuestionList(info.questions);
      setIsLoading(false);
    });
  }, []);

  const startSession = () => {
    setCurrentQuestion(questionList[0]);
    setQuestionNum(0);
    setHasStarted(true);
    setCurrentQuestion(questionList[questionNum]);
    setState("Preparing");
    startPrepPhase();
  };
  const finishSession = () => {
    setFinishModalUp(true);
  };
  const startPrepPhase = () => {
    setContinueModalUp(false);

    // setting the next question
    setCurrentQuestion(questionList[questionNum]);
    timer.start(true);
    timer.addCallback(() => {
      startRecordingPhase();
    }, prepPhaseDurtion);
  };

  const startRecordingPhase = () => {
    setState("Recording");

    timer.start(true);
    recording.startRecording();
    timer.addCallback((_elap: number) => {
      endRecordingPhase();
    }, recordingPhaseDuration);
  };
  const endRecordingPhase = () => {
    setState("Preparing");
    recording.endRecording();

    sendRecording(recording.recordedChunks).then((res) => {
      if (res == "Ok") {
        setVideosUploaded((prev) => prev + 1);
      }
    });
    setQuestionNum((prev) => {
      return prev + 1;
    });
    if (questionNum == questionList.length - 1) {
      finishSession();
    } else {
      setContinueModalUp(true);
    }
    timer.pause();
  };
  const toggleRecording = () => {
    // cannot pause preparing
    if (state == "Preparing") {
      return;
    }
    recording.toggleRecording();
    if (timer.running) {
      timer.pause();
    } else {
      timer.start();
    }
  };
  const recordingDuration = () => {
    if (state == "Recording") {
      return timer.elapsed / 1000;
    }
    return 0;
  };

  return {
    finishModalUp: finishModalUp,
    startNextQuestion: startPrepPhase,
    continueModalUp: continueModalUp,
    videosUploadedCount: videosUploaded,
    timerDisplay: timer.elapsed / 1000,
    currentQuestion: currentQuestion,
    webcam: recording.webRef,
    recordingDuration: recordingDuration(),
    isInitalLoading: isLoading,
    state: state,
    hasStarted: hasStarted,
    totalQuestions: questionList.length,
    currentQuestionNumber: questionNum,
    isRecording: recording.capturing,
    toggleRecording: toggleRecording,
    startSession: startSession,
  };
}
export default useSession;
