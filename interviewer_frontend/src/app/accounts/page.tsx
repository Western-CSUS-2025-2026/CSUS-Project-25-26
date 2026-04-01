"use client";

import { useState } from "react";
import LoginCard from "./_components/loginCard";
import CreateAccountEmailCard from "./_components/createAccountEmail";
import CreateAccountCode from "./_components/createAccountCode";
import CreateAccountCard from "./_components/createAccountName";
import CreateAccountPassword from "./_components/createAccountPassword";

type Mode =
  | "login"
  | "signup-email"
  | "signup-code"
  | "signup-details"
  | "signup-password";

export default function AccountsPage() {
  const [mode, setMode] = useState<Mode>("login");

  // state carried over
  const [signupEmail, setSignupEmail] = useState("");
  const [signupCode, setSignupCode] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  return (
    <div>
      {mode === "login" && (
        <LoginCard onSignUp={() => setMode("signup-email")} />
      )}

      {mode === "signup-email" && (
        <CreateAccountEmailCard
          onNext={(email) => {
            setSignupEmail(email);
            setMode("signup-code");
          }}
          onBackToLogin={() => setMode("login")}
        />
      )}

      {mode === "signup-code" && (
        <CreateAccountCode
          email={signupEmail}
          onNext={(code) => {
            setSignupCode(code);
            setMode("signup-details");
          }}
          onBackToLogin={() => setMode("signup-email")}
        />
      )}

      {mode === "signup-details" && (
        <CreateAccountCard
          onBack={() => setMode("signup-code")}
          onNext={(first, last) => {
            setFirstName(first);
            setLastName(last);
            setMode("signup-password");
          }}
        />
      )}

      {mode === "signup-password" && (
        <CreateAccountPassword
          email={signupEmail}
          code={signupCode}
          firstName={firstName}
          lastName={lastName}
          onBack={() => setMode("signup-details")}
          onNext={() => {
            setMode("login");
          }}
        />
      )}
    </div>
  );
}
