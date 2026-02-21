"use client";

import React, { useRef, useState } from "react";
import Card from "@/components/card/card";
import styles from "./loginCard.module.css";
import codeStyles from "./createAccountCode.module.css";

interface CreateAccountCodeProps {
  onNext: () => void;
  onBackToLogin: () => void;
  email?: string;
}

export default function CreateAccountCode({
  onNext,
  onBackToLogin,
  email = "email@uwo.ca",
}: CreateAccountCodeProps) {
  const CODE_LEN = 6;

  const [digits, setDigits] = useState<string[]>(Array(CODE_LEN).fill(""));
  const inputRefs = useRef<Array<HTMLInputElement | null>>([]);

  const setRef =
    (index: number) =>
    (el: HTMLInputElement | null): void => {
      inputRefs.current[index] = el;
    };

  const focusIndex = (i: number) => {
    inputRefs.current[i]?.focus();
    inputRefs.current[i]?.select();
  };

  const handleChange = (index: number, value: string) => {
    const v = value.replace(/\D/g, "");

    // If user pastes/types multiple digits into one box
    if (v.length > 1) {
      const next = [...digits];
      for (let k = 0; k < v.length && index + k < CODE_LEN; k++) {
        next[index + k] = v[k];
      }
      setDigits(next);

      const nextFocus = Math.min(index + v.length, CODE_LEN - 1);
      focusIndex(nextFocus);
      return;
    }

    const next = [...digits];
    next[index] = v;
    setDigits(next);

    if (v && index < CODE_LEN - 1) focusIndex(index + 1);
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace") {
      if (digits[index]) {
        // Clear current digit
        const next = [...digits];
        next[index] = "";
        setDigits(next);
      } else if (index > 0) {
        // Move left and clear previous
        const next = [...digits];
        next[index - 1] = "";
        setDigits(next);
        focusIndex(index - 1);
      }
      return;
    }

    if (e.key === "ArrowLeft" && index > 0) {
      focusIndex(index - 1);
      return;
    }

    if (e.key === "ArrowRight" && index < CODE_LEN - 1) {
      focusIndex(index + 1);
      return;
    }
  };

  const handlePaste = (e: React.ClipboardEvent<HTMLDivElement>) => {
    const pasted = e.clipboardData
      .getData("text")
      .replace(/\D/g, "")
      .slice(0, CODE_LEN);

    if (!pasted) return;

    e.preventDefault();

    const next = Array(CODE_LEN).fill("");
    for (let i = 0; i < pasted.length; i++) next[i] = pasted[i];
    setDigits(next);

    focusIndex(Math.min(pasted.length, CODE_LEN) - 1);
  };

  const code = digits.join("");
 
  return (
    <>
      <div className={styles.container}>
        <div className="loginCardRadiusOverride">
          <div className={styles.sizeBox}>
            <Card fillHeight fillWidth>
              <h1 className={styles.header}>Create Account</h1>

              <div className={styles.coloumn}>
                <div className={styles.line}></div>

                <p className={codeStyles.sendingText}>
                  We've sent a 6-digit code to{" "}
                  <span className={codeStyles.email}>{email}</span>. Please enter it
                  below.
                </p>

                <p className={codeStyles.codeText}>6-digit code</p>

                <div className={codeStyles.codeRow} onPaste={handlePaste}>
                  {digits.map((digit, index) => (
                    <input
                      key={index}
                      ref={setRef(index)}
                      className={codeStyles.digitBox}
                      value={digit}
                      inputMode="numeric"
                      autoComplete={index === 0 ? "one-time-code" : "off"}
                      maxLength={1}
                      onChange={(e) => handleChange(index, e.target.value)}
                      onKeyDown={(e) => handleKeyDown(index, e)}
                      aria-label={`Digit ${index + 1}`}
                    />
                  ))}
                </div>

                  <button
                    type="button"
                    className={codeStyles.ResendText}
                    onClick={() => {
                    }}
                  >
                    Resend Code
                  </button>

                <button
                  className={styles.loginButton}
                  type="button"
                  onClick={onNext}
                >
                  Next
                </button>

                <div>
                  <button
                    type="button"
                    className={styles.linkButton}
                    onClick={onBackToLogin}
                  >
                    Back
                  </button>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>

      <style>{`
        .loginCardRadiusOverride .cardStyle {
          border-radius: 2em !important;
        }
      `}</style>
    </>
  );
}