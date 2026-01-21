"use client";
import Card from "@/components/card/card";
import Webcam from "react-webcam";
import styles from "./webcamCard.module.css";
import { RefObject } from "react";

interface WebcamCardProps {
  webRef: RefObject<Webcam | null>;
}

const videoConstraints = {
  width: 630,
  height: 440,
  facingMode: "user",
};

function WebcamCard({ webRef }: WebcamCardProps) {
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
