"use client";

import React, { useRef, useState } from "react";
import { useActionState } from "react";
import Card from "@/components/card/card";
import styles from "./loginCard.module.css";
import codeStyles from "./createAccountCode.module.css";
import {
  checkVerificationCode,
  type CheckVerificationCodeResponse,
} from "@/actions/login/register";

interface CreateAccountCodeProps {
  onNext: (code: string) => void; // pass code upward
  onBackToLogin: () => void;
  email?: string;
}

export default function CreateAccountCode({
  onNext,
  onBackToLogin,
  email,
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

    if (v.length > 1) {
      const next = [...digits];
      for (let k = 0; k < v.length && index + k < CODE_LEN; k++) {
        next[index + k] = v[k];
      }
      setDigits(next);
      focusIndex(Math.min(index + v.length, CODE_LEN - 1));
      return;
    }

    const next = [...digits];
    next[index] = v;
    setDigits(next);

    if (v && index < CODE_LEN - 1) focusIndex(index + 1);
  };

  const handleKeyDown = (
    index: number,
    e: React.KeyboardEvent<HTMLInputElement>,
  ) => {
    if (e.key === "Backspace") {
      if (digits[index]) {
        const next = [...digits];
        next[index] = "";
        setDigits(next);
      } else if (index > 0) {
        const next = [...digits];
        next[index - 1] = "";
        setDigits(next);
        focusIndex(index - 1);
      }
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
  const isComplete = digits.every((d) => d.length === 1);

  const [result, formAction, isPending] = useActionState<
    CheckVerificationCodeResponse | undefined,
    FormData
  >(async (_prev, formData) => {
    // block incomplete codes
    const submittedCode = String(formData.get("code") ?? "");
    const submittedEmail = String(formData.get("email") ?? "");

    if (!submittedEmail || submittedCode.length !== CODE_LEN) {
      return "INVALID_FORM";
    }

    const res = await checkVerificationCode(undefined, formData);

    // Only move on if backend says SUCCESS
    if (res === "SUCCESS") {
      onNext(submittedCode);
    }

    return res;
  }, undefined);

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
                  <span className={codeStyles.email}>{email}</span>. Please enter
                  it below.
                </p>

                <form action={formAction} noValidate>
                  <input type="hidden" name="email" value={email ?? ""} />
                  <input type="hidden" name="code" value={code} />

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
                        disabled={isPending}
                        aria-label={`Digit ${index + 1}`}
                      />
                    ))}
                  </div>

                  <div className={styles.loginWrapper}>
                    <button
                      className={styles.loginButton}
                      type="submit"
                      disabled={isPending || !isComplete} 
                    >
                      {isPending ? "Verifying..." : "Next"}
                    </button>

                    {result && result !== "SUCCESS" && (
                      <div className={styles.errorText} role="status">
                        {result === "INVALID_FORM" && "Enter the full 6-digit code."}
                        {result === "INVALID_CODE" && "That code is incorrect or expired."}
                        {result === "NETWORK_ERROR" && "Network error. Try again."}
                      </div>
                    )}
                  </div>
                </form>

                <div>
                  <button
                    type="button"
                    className={styles.linkButton}
                    onClick={onBackToLogin}
                    disabled={isPending}
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