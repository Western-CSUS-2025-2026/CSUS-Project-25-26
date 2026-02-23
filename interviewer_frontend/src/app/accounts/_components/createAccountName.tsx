"use client";

import Card from "@/components/card/card";
import styles from "./loginCard.module.css";
import { useState } from "react";

interface CreateAccountCardProps {
  onBack: () => void;
  onNext: (firstName: string, lastName: string) => void;
}

export default function CreateAccountCard({ onBack, onNext }: CreateAccountCardProps) {
  const [error, setError] = useState<string | null>(null);

  return (
    <>
      <div className={styles.container}>
        <div className="loginCardRadiusOverride">
          <div className={styles.sizeBox}>
            <Card fillHeight fillWidth>
              <h1 className={styles.header}>Create Account</h1>

              <div className={styles.coloumn}>
                <div className={styles.line}></div>

                <form
                  noValidate
                  onSubmit={(e) => {
                    e.preventDefault();
                    setError(null);

                    const fd = new FormData(e.currentTarget);
                    const firstName = String(fd.get("firstName") ?? "").trim();
                    const lastName = String(fd.get("lastName") ?? "").trim();

                    if (!firstName || !lastName) {
                      setError("Please fill out both names.");
                      return;
                    }

                    onNext(firstName, lastName);
                  }}
                >
                  <div className={styles.infoBox}>
                    <p>First Name</p>
                    <input
                      name="firstName"
                      type="text"
                      className={styles.textBox}
                      placeholder="Enter your first name"
                      autoComplete="given-name"
                    />

                    <p>Last Name</p>
                    <input
                      name="lastName"
                      type="text"
                      className={styles.textBox}
                      placeholder="Enter your last name"
                      autoComplete="family-name"
                    />
                  </div>

                  <div className={styles.loginWrapper}>
                    <button className={styles.loginButton} type="submit">
                      Next
                    </button>

                    {error && (
                      <div className={styles.errorText} role="status">
                        {error}
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