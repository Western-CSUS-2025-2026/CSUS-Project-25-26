"use client";

import { useState } from "react";
import LoginCard from "./_components/loginCard";
import CreateAccountEmailCard from "./_components/createAccountEmail";
import CreateAccountCard from "./_components/createAccountName";

type Mode = "login" | "signup-email" | "signup-details";

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
          onNext={() => setMode("signup-details")}
          onBackToLogin={() => setMode("login")}
        />
      )}

      {mode === "signup-details" && (
        <CreateAccountCard
          onBack={() => setMode("signup-email")}
          onNext={() => {
            // submit signup or go to next step
          }}
        />
      )}
    </div>
  );
}
