"use client";

import { useActionState } from "react";
import Card from "@/components/card/card";
import styles from "./loginCard.module.css";
import { login, type LoginResponse } from "@/actions/login/login";

interface LoginCardProps {
  onSignUp: () => void;
}

export default function LoginCard({ onSignUp }: LoginCardProps) {
  const [result, formAction, isPending] = useActionState<LoginResponse | undefined, FormData>(
    async (_prevState, formData) => {
      return await login(formData);
    },
    undefined
  );

  return (
    <>
      <div className={styles.container}>
        <div className="loginCardRadiusOverride">
          <div className={styles.sizeBox}>
            <Card fillHeight fillWidth>
              <h1 className={styles.header}>Login</h1>

              <div className={styles.coloumn}>
                <div className={styles.line}></div>

                <form action={formAction}>
                  <div className={styles.infoBox}>
                    <p>Email</p>
                    <input
                      name="email"
                      type="email"
                      className={styles.textBox}
                      placeholder="Enter your email"
                      autoComplete="email"
                    />

                    <p>Password</p>
                    <input
                      name="password"
                      type="password"
                      className={styles.textBox}
                      placeholder="Enter your password"
                      autoComplete="current-password"
                    />
                  </div>

                  <div className={styles.loginWrapper}>
                    <button
                      className={styles.loginButton}
                      type="submit"
                      disabled={isPending}
                    >
                      {isPending ? "Logging in..." : "Login"}
                    </button>

                    {result && result !== "SUCCESS" && (
                      <div className={styles.errorText}>
                        {result === "NOT_AUTHORIZED" && "Email or password is incorrect."}
                        {result === "NETWORK_ERROR" && "Network error. Try again."}
                        {result === "UNVALID_FORM" && "Please fill out all fields."}
                      </div>
                    )}
                  </div>

                </form>

                <div className={styles.linkText}>
                  <button type="button" className={styles.linkButton}>
                    Forgot Password
                  </button>

                  <button
                    type="button"
                    className={styles.linkButton}
                    onClick={onSignUp}
                  >
                    Sign Up
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