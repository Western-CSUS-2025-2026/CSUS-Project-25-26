"use client";
import Card from "@/components/card/card";
import Webcam from "react-webcam";
import styles from "./webcamCard.module.css";
import { RefObject } from "react";

interface WebcamCardProps {
  webRef: RefObject<Webcam | null>;
}

const videoConstraints = {
  width: 700,
  height: 500,
  facingMode: "user",
};

function WebcamCard({ webRef }: WebcamCardProps) {
  return (
    <Card>
      <Webcam
        className={styles.webcam}
        ref={webRef}
        videoConstraints={videoConstraints}
      />
    </Card>
  );
}

export default WebcamCard;
