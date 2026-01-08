"use client";
import {
  checkVerificationCode,
  getVerificationEmail,
} from "@/actions/login/register";
import Card from "@/components/card/card";
import LoadingText from "@/components/loadingText/loadingText";
import { useActionState, useRef } from "react";

export default function Home() {
  const [state, formAction] = useActionState(getVerificationEmail, undefined);
  const [codeState, codeFormAction] = useActionState(
    checkVerificationCode,
    undefined,
  );

  const fromFunc = async () => {
    const form = new FormData();
    form.append("email", "test");
    const res = await getVerificationEmail(undefined, form);
  };

  return (
    <div>
      <Card height="30em" width="20em">
        <p>
          The pt size is what it is in the figma to help you decide what to use
        </p>
        <h1>Heading 1 (30 pt)</h1>
        <h2>Heading 2 (25 pt)</h2>
        <h3>Heading 3 (20 pt)</h3>
        <p>Paragraph (16 pt)</p>

        <div style={{ display: "flex", flexDirection: "row" }}>
          <LoadingText width="10em" loading presetHeight="H2">
            <h2>Test</h2>
          </LoadingText>
          <div style={{ width: "3em" }}></div>
          <LoadingText width="10em" presetHeight="H2">
            <h2>Test</h2>
          </LoadingText>
        </div>
      </Card>
      <Card>
        <form action={formAction}>
          <input name="email" />
          <button style={{ color: "green" }} type="submit">
            Submit Form
          </button>
          <div style={{ color: "green" }}>{state}</div>
        </form>
        <div> Code</div>
        <form action={codeFormAction}>
          <input name="email" />
          <input name="code" />
          <button style={{ color: "green" }} type="submit">
            Submit Form
          </button>
          <div style={{ color: "green" }}>{codeState}</div>
        </form>
      </Card>
    </div>
  );
}
