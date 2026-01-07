"use client";
import { RefObject, useCallback, useRef, useState } from "react";
import Webcam from "react-webcam";

interface UseRecordingReturn {
  webRef: RefObject<Webcam | null>;
  capturing: boolean;
  recordedChunks: Blob[];
  startRecording: () => void;
  endRecording: () => void;
  download: () => void;
}

export function useRecording(): UseRecordingReturn {
  const webRef = useRef<Webcam>(null);
  const mediaRef = useRef<MediaRecorder>(null);
  const [capturing, setCapturing] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState<Blob[]>([]);

  const handleData = useCallback(
    ({ data }: BlobEvent) => {
      if (data.size > 0) {
        setRecordedChunks((prev) => prev.concat(data));
      }
    },
    [setRecordedChunks],
  );

  const startRecording = useCallback(() => {
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
    mediaRef.current.start();
  }, [webRef, setCapturing, mediaRef, handleData]);

  const endRecording = useCallback(() => {
    mediaRef.current?.stop();
    setCapturing(false);
  }, [setCapturing, mediaRef]);
  const handleDownload = useCallback(() => {
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
  }, [recordedChunks]);
  return {
    webRef: webRef,
    recordedChunks: recordedChunks,
    startRecording: startRecording,
    endRecording: endRecording,
    capturing: capturing,

    download: handleDownload,
  };
}
