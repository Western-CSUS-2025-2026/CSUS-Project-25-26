"use client";

import React, { useMemo, useState } from "react";
import { useActionState } from "react";
import Card from "@/components/card/card";
import styles from "./loginCard.module.css";
import passStyles from "./createAccountPassword.module.css";
import {
  completeRegistration,
  type RegistrationResponse,
} from "@/actions/login/register";

interface CreateAccountPasswordProps {
  onBack: () => void;
  onNext: () => void;

  email: string;
  code: string;
  firstName: string;
  lastName: string;
}

export default function CreateAccountPassword({
  onBack,
  onNext,
  email,
  code,
  firstName,
  lastName,
}: CreateAccountPasswordProps) {
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const checks = useMemo(() => {
    const has8 = password.length >= 8;
    const hasNumber = /\d/.test(password);
    const hasSymbol = /[^A-Za-z0-9]/.test(password);
    return { has8, hasNumber, hasSymbol };
  }, [password]);

  //clickable when it meets the 3 requirements 
  const canProceed = checks.has8 && checks.hasNumber && checks.hasSymbol;

  const [result, formAction, isPending] = useActionState<
    RegistrationResponse | undefined,
    FormData
  >(async (_prev, formData) => {
    const res = await completeRegistration(undefined, formData);

    if (res === "SUCCESS") {
      onNext();
      return res;
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

                <form action={formAction} noValidate>
                  {/*send everything */}
                  <input type="hidden" name="email" value={email} />
                  <input type="hidden" name="code" value={code} />
                  <input type="hidden" name="firstName" value={firstName} />
                  <input type="hidden" name="lastName" value={lastName} />

                  <div className={styles.infoBox}>
                    <p className={passStyles.noTopMargin}>Password</p>
                    <input
                      name="password"
                      type="password"
                      className={styles.textBox}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      autoComplete="new-password"
                    />

                    <div className={passStyles.passwordRequirements}>
                      Your password must contain at least:
                    </div>

                    <div
                      className={`${passStyles.passwordRequirementsList} ${
                        checks.has8 ? passStyles.met : passStyles.unmet
                      }`}
                    >
                      8 characters
                    </div>

                    <div
                      className={`${passStyles.passwordRequirementsList} ${
                        checks.hasNumber ? passStyles.met : passStyles.unmet
                      }`}
                    >
                      1 number
                    </div>

                    <div
                      className={`${passStyles.passwordRequirementsList} ${
                        checks.hasSymbol ? passStyles.met : passStyles.unmet
                      }`}
                    >
                      1 symbol
                    </div>

                    <div className={passStyles.reEnter}>Re-enter Password</div>
                    <input
                      name="password-confim" // ✅ must match register.ts spelling
                      type="password"
                      className={styles.textBox}
                      value={confirm}
                      onChange={(e) => setConfirm(e.target.value)}
                      autoComplete="new-password"
                    />
                  </div>

                  {/* error belwo button*/}
                  <div className={styles.loginWrapper}>
                    <button
                      className={passStyles.loginButton}
                      type="submit"
                      disabled={!canProceed || isPending}
                    >
                      {isPending ? "Creating..." : "Next"}
                    </button>

                    {result && result !== "SUCCESS" && (
                      <div className={styles.errorText} role="status">
                        {result === "PASSWORDS_DONT_MATCH" &&
                          "Passwords do not match."}

                        {/* retry error */}
                        {result !== "PASSWORDS_DONT_MATCH" &&
                          "Network error. Try again."}
                      </div>
                    )}
                  </div>
                </form>

                <div>
                  <button
                    type="button"
                    className={styles.linkButton}
                    onClick={onBack}
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