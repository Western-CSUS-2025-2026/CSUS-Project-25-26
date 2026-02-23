"use client";

import React, { useMemo, useState } from "react";
import Card from "@/components/card/card";
import styles from "./loginCard.module.css";
import passStyles from "./createAccountPassword.module.css";

interface CreateAccountPasswordProps {
  onBack: () => void;
  onNext: () => void;
}

export default function CreateAccountPassword({
  onBack,
  onNext,
}: CreateAccountPasswordProps) {
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const checks = useMemo(() => {
    const has8 = password.length >= 8;
    const hasNumber = /\d/.test(password);
    const hasSymbol = /[^A-Za-z0-9]/.test(password); // anything not letter/number
    const matches = confirm.length > 0 && password === confirm;

    return { has8, hasNumber, hasSymbol, matches };
  }, [password, confirm]);

  const canProceed =
    checks.has8 && checks.hasNumber && checks.hasSymbol && checks.matches;

  return (
    <>
      <div className={styles.container}>
        <div className="loginCardRadiusOverride">
          <div className={styles.sizeBox}>
            <Card fillHeight fillWidth>
              <h1 className={styles.header}>Create Account</h1>

              <div className={styles.coloumn}>
                <div className={styles.line}></div>

                <div className={styles.infoBox}>
                  <p className={passStyles.noTopMargin}>Password</p>
                  <input
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
                    type="password"
                    className={styles.textBox}
                    value={confirm}
                    onChange={(e) => setConfirm(e.target.value)}
                    autoComplete="new-password"
                  />
                </div>

                <button
                  className={passStyles.loginButton}
                  type="button"
                  onClick={onNext}
                  disabled={!canProceed}
                >
                  Next
                </button>

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