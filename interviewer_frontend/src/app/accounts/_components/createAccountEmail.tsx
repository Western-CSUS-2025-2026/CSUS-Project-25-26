"use client";

import { useActionState } from "react";
import Card from "@/components/card/card";
import styles from "./loginCard.module.css";
import {
  getVerificationEmail,
  type GetVerificationEmailResponse,
} from "@/actions/login/register";

interface CreateAccountEmailCardProps {
  onNext: (email: string) => void;
  onBackToLogin: () => void;
}

export default function CreateAccountEmailCard({
  onNext,
  onBackToLogin,
}: CreateAccountEmailCardProps) {
  const [result, formAction, isPending] = useActionState<
    GetVerificationEmailResponse | undefined,
    FormData
  >(async (_prev, formData) => {
    const raw = formData.get("email");
    const email = typeof raw === "string" ? raw : "";

    // if empty
    if (email === "") return "INVALID_FORM";

    const res = await getVerificationEmail(undefined, formData);

    const Bypass = process.env.NODE_ENV === "development";

    if (res === "SUCCESS") {
      onNext(email);
      return res;
    }

    // bypass errors from api 
    if (Bypass) {
      console.warn("[BYPASS]", res);
      onNext(email);
      return "SUCCESS"; 
    }

    // use real backend result once api call works
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
                  <div className={styles.infoBox}>
                    <p>Email</p>
                    <input
                      name="email"
                      type="email"
                      className={styles.textBox}
                      placeholder="Enter your email"
                      autoComplete="email"
                      required
                      aria-invalid={result && result !== "SUCCESS" ? true : undefined}
                    />
                  </div>

                  <div className={styles.blankSpace}></div>

                  <div className={styles.loginWrapper}>
                    <button
                      className={styles.loginButton}
                      type="submit"
                      disabled={isPending}
                    >
                      {isPending ? "Sending..." : "Next"}
                    </button>

                    {result && result !== "SUCCESS" && (
                      <div className={styles.errorText} role="status">
                        {result === "INVALID_FORM" && "Please enter your email."}
                        {result === "INVALID_EMAIL" && "That email is not valid."}
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