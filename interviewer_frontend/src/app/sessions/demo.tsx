"use client";

import Modal from "@/components/modal/modal";
import styles from "./page.module.css";
import { useRouter } from "next/navigation";
import { createSession } from "@/lib/sessionLib/createSession";

function DemoModal() {
  const ID = 10;
  const router = useRouter();
  const onClick = () => {
    createSession(Number(ID)).then((res) => {
      if (res.success) {
        router.push(`/recording?sessionId=${res.sessionId}`);
      }
    });
  };
  return (
    <Modal>
      <div className={styles.startContainer}>
        <h1>Getting Started </h1>
        <p style={{ marginBottom: "3em" }}>
          Try out our interviewer prepper with a curated demo template.
        </p>
        <div className={styles.selectedCard}>
          <div className={styles.selectedTitle}>{"Demo Template"}</div>
          <div className={styles.selectedSubtitle}>
            {"A special template to show off the power of our interviewer tool"}
          </div>
        </div>

        <button onClick={onClick} className={styles.startButton}>
          Start Here
        </button>
      </div>
    </Modal>
  );
}

export default DemoModal;
