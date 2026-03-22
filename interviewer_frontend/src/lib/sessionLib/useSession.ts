"use client";
import { RefObject, useEffect, useState } from "react";
import { useRecording } from "./useRecording";
import Webcam from "react-webcam";
import { useTimer } from "./useTimer";
import { Question } from "./getQuestions";
import { sendRecording } from "./sendRecording";
import { getSessionNew } from "../getNewSession";
import fixWebmDuration from "fix-webm-duration";

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
  prepPhaseDurtion: number;
  recordingPhaseDuration: number;
}

function useSession(sessionId: number): UseSessionReturn {
  const prepPhaseDurtion = 10000;
  const recordingPhaseDuration = 30000;
  const recording = useRecording();
  const [questionList, setQuestionList] = useState<Question[]>([]);
  const [questionNum, setQuestionNum] = useState(0);
  const [videosUploaded, setVideosUploaded] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState<Question>({
    question: "Start and questions will appear here...",
    id: -1,
    template_id: -1,
    component_id: -1,
  });

  const timer = useTimer();

  const [finishModalUp, setFinishModalUp] = useState(false);
  const [continueModalUp, setContinueModalUp] = useState(false);

  const [isLoading, setIsLoading] = useState(true);
  const [state, setState] = useState<SessionState>("Preparing");
  const [hasStarted, setHasStarted] = useState(false);

  useEffect(() => {
    getSessionNew(Number(sessionId)).then((s) => {
      if (s.success) {
        const questions: Question[] = s.session.session_components.map(
          (com) => {
            return {
              question: com.question.question,
              component_id: com.id,
              id: com.question.id,
              template_id: com.question.template_id,
            };
          },
        );
        setQuestionList(questions);
        setIsLoading(false);
      }
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
    recording.endRecording((chunk) => {
      const fixed = chunk;
      const video = document.createElement("video");
      video.onloadedmetadata = () => {
        console.log("Duration " + video.duration);
      };

      video.src = URL.createObjectURL(fixed);

      sendRecording(questionList[questionNum].component_id, fixed).then(
        (res) => {
          if (res == "Ok") {
            setVideosUploaded((prev) => prev + 1);
          }
        },
      );
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
    currentQuestion: currentQuestion.question,
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
    prepPhaseDurtion: prepPhaseDurtion,
    recordingPhaseDuration: recordingPhaseDuration,
  };
}
export default useSession;
