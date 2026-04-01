"use client";

import dynamic from "next/dynamic";
import Modal from "../modal/modal";
import styles from "./safariWarning.module.css";

function SafariWarning() {
  const isSafariBrowser = /^((?!chrome|android).)*safari/i.test(
    navigator.userAgent,
  );

  if (!isSafariBrowser) return null;

  return (
    <Modal width="400px" flexDirection="column" alignItems="center">
      <div className={styles.container}>
        <h2 className={styles.title}>Browser Compatibility Notice</h2>
        <p className={styles.message}>
          Safari is not officially supported. For the best experience, please
          use Chrome, Firefox, or Edge.
        </p>
        <p className={styles.subtitle}>
          Some features may not work as expected.
        </p>
      </div>
    </Modal>
  );
}
export const SafariWarningNoSSR = dynamic(() => import("./safariWarning"), {
  ssr: false,
});

export default SafariWarning;
