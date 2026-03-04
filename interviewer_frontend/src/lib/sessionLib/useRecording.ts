"use client";
import { RefObject, useRef, useState } from "react";
import Webcam from "react-webcam";

interface UseRecordingReturn {
  webRef: RefObject<Webcam | null>;
  capturing: boolean;
  recordedChunks: Blob[];
  startRecording: () => void;
  endRecording: () => Blob[];
  download: () => void;
  toggleRecording: () => void;
  startTime: Date | undefined;
  endTime: Date | undefined;
}

export function useRecording(): UseRecordingReturn {
  const webRef = useRef<Webcam>(null);
  const mediaRef = useRef<MediaRecorder>(null);
  const chunksRef = useRef<Blob[]>([]);
  const [capturing, setCapturing] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState<Blob[]>([]);
  const [startTime, setStartTime] = useState<undefined | Date>();
  const [endTime, setEndTime] = useState<undefined | Date>();
  const toggleRecording = () => {
    setCapturing(!capturing);
  };

  const handleData = ({ data }: BlobEvent) => {
    if (data.size > 0) {
      chunksRef.current.push(data);
      setRecordedChunks((prev) => prev.concat(data));
    }
  };

  const startRecording = () => {
    setStartTime(new Date());
    setEndTime(undefined);
    chunksRef.current = [];
    setRecordedChunks([]);
    setCapturing(true);
    if (webRef.current == null) {
      console.log("Web ref is null");
      return;
    }
    if (mediaRef == null) {
      console.log("Media ref is null");
      return;
    }
    if (webRef.current.stream == null) {
      console.log("Web stream is not accessible");
      return;
    }
    mediaRef.current = new MediaRecorder(webRef.current.stream, {
      mimeType: "video/webm",
    });

    mediaRef.current.addEventListener("dataavailable", handleData);
    mediaRef.current.start(1000);
  };
  const endRecording = (): Blob[] => {
    setEndTime(new Date());
    mediaRef.current?.stop();
    setCapturing(false);
    return chunksRef.current;
  };
  const handleDownload = () => {
    if (recordedChunks.length) {
      const blob = new Blob(recordedChunks, {
        type: "video/webm",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      document.body.appendChild(a);
      a.style = "display: none";
      a.href = url;
      a.download = "react-webcam-stream-capture.webm";
      a.click();
      window.URL.revokeObjectURL(url);
      setRecordedChunks([]);
    }
  };
  return {
    toggleRecording: toggleRecording,
    webRef: webRef,
    recordedChunks: recordedChunks,
    startRecording: startRecording,
    endRecording: endRecording,
    capturing: capturing,
    endTime: endTime,
    startTime: startTime,
    download: handleDownload,
  };
}
