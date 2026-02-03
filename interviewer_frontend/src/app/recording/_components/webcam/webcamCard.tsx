"use client";
import Card from "@/components/card/card";
import Webcam from "react-webcam";
import styles from "./webcamCard.module.css";
import { RefObject } from "react";
import { useWindowDimensions } from "@/lib/useWindowDimensions";

interface WebcamCardProps {
  webRef: RefObject<Webcam | null>;
}

function WebcamCard({ webRef }: WebcamCardProps) {
  const dims = useWindowDimensions();
  const videoConstraints = {
    width: 0.5 * dims.width,
    height: (440 / 717) * dims.height,
    facingMode: "user",
  };

  return (
    <Card>
      <Webcam
        audio={true}
        className={styles.webcam}
        ref={webRef}
        videoConstraints={videoConstraints}
      />
    </Card>
  );
}

export default WebcamCard;
