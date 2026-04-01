"use client";

import { createPortal } from "react-dom";
import Modal from "@/components/modal/modal";
import styles from "./demo.module.css";
import { useRouter } from "next/navigation";
import { createSession } from "@/lib/sessionLib/createSession";
import dynamic from "next/dynamic";

function DemoModal() {
  const ID = 4;
  const router = useRouter();
  const onClick = () => {
    createSession(Number(ID)).then((res) => {
      if (res.success) {
        router.push(`/recording?sessionId=${res.sessionId}`);
      }
    });
  };

  const modalContent = (
    <Modal width="500px" flexDirection="column" alignItems="center">
      <div className={styles.container}>
        {/* Header */}
        <div className={styles.header}>
          <h1 className={styles.title}>Welcome to Jobless.live</h1>
          <p className={styles.subtitle}>
            Get started in 30 seconds with our interactive demo
          </p>
        </div>

        {/* Features List */}
        <div className={styles.featuresSection}>
          <h2 className={styles.sectionTitle}>{"What you'll experience:"}</h2>
          <ul className={styles.featuresList}>
            <li className={styles.featureItem}>
              <div>
                <div className={styles.featureName}>Practice Speaking</div>
                <div className={styles.featureDesc}>
                  Answer interview questions aloud
                </div>
              </div>
            </li>
            <li className={styles.featureItem}>
              <div>
                <div className={styles.featureName}>Get Feedback</div>
                <div className={styles.featureDesc}>
                  Receive detailed analysis on delivery
                </div>
              </div>
            </li>
            <li className={styles.featureItem}>
              <div>
                <div className={styles.featureName}>Track Progress</div>
                <div className={styles.featureDesc}>
                  Improve with every practice session
                </div>
              </div>
            </li>
          </ul>
        </div>

        {/* Demo Template Card */}
        <div className={styles.demoCard}>
          <div className={styles.cardBadge}>Demo Template</div>
          <div className={styles.cardTitle}>Sample Interview</div>
          <div className={styles.cardDescription}>
            A curated set of common interview questions to help you get familiar
            with the platform
          </div>
        </div>

        {/* CTA Button */}
        <button onClick={onClick} className={styles.startButton}>
          <span>Start Demo</span>
          <span className={styles.arrow}>→</span>
        </button>
      </div>
    </Modal>
  );

  return createPortal(modalContent, document.body);
}

export const DemoModalNoSSR = dynamic(() => import("./demo"), {
  ssr: false,
});

export default DemoModal;
