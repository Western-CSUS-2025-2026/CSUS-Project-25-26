"use client";

import { useState } from "react";
import LoginCard from "./_components/loginCard";
import CreateAccountEmailCard from "./_components/createAccountEmail";
import CreateAccountCard from "./_components/createAccountName";
import CreateAccountCode from "./_components/createAccountCode";

type Mode = "login" | "signup-email" | "signup-code" | "signup-details";

export default function AccountsPage() {
  const [mode, setMode] = useState<Mode>("login");

  return (
    <div>
      {mode === "login" && (
        <LoginCard
          onSignUp={() => setMode("signup-email")}
        />
      )}

      {mode === "signup-email" && (
        <CreateAccountEmailCard
          onNext={() => setMode("signup-code")}
          onBackToLogin={() => setMode("login")}
        />
      )}

      {mode === "signup-code" && (
        <CreateAccountCode
          email="ysahota@uwo.ca"
          onNext={() => setMode("signup-details")}
          onBackToLogin={() => setMode("signup-email")}
        />
      )}

      {mode === "signup-details" && (
        <CreateAccountCard
          onBack={() => setMode("signup-code")}
          onNext={() => {
            // submit signup or go to next step
          }}
        />
      )}
    </div>
  );
}
