"use client";

import { useState } from "react";
import LoginCard from "./_components/loginCard";
import CreateAccountEmailCard from "./_components/createAccountEmail";
import CreateAccountCard from "./_components/createAccountName";
import CreateAccountCode from "./_components/createAccountCode";
import CreateAccountPassword from "./_components/createAccountPassword";

type Mode =
  | "login"
  | "signup-email"
  | "signup-code"
  | "signup-details"
  | "signup-password";

export default function AccountsPage() {
  const [mode, setMode] = useState<Mode>("login");
  const [signupEmail, setSignupEmail] = useState<string>(""); // store email here

  return (
    <div>
      {mode === "login" && <LoginCard onSignUp={() => setMode("signup-email")} />}

      {mode === "signup-email" && (
        <CreateAccountEmailCard
          onNext={(email) => {
            setSignupEmail(email);     // save email 
            setMode("signup-code");    
          }}
          onBackToLogin={() => setMode("login")}
        />
      )}

      {mode === "signup-code" && (
        <CreateAccountCode
          email={signupEmail}          //use saved email
          onNext={() => setMode("signup-details")}
          onBackToLogin={() => setMode("signup-email")}
        />
      )}

      {mode === "signup-details" && (
        <CreateAccountCard
          onBack={() => setMode("signup-code")}
          onNext={() => setMode("signup-password")}
        />
      )}

      {mode === "signup-password" && (
        <CreateAccountPassword
          onBack={() => setMode("signup-details")}
          onNext={() => {
            // later: call completeRegistration here
          }}
        />
      )}
    </div>
  );
}