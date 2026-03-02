"use server";
import { fetchAPI } from "@/lib/fetch";

export type GetVerificationEmailResponse =
  | "SUCCESS"
  | "NETWORK_ERROR"
  | "INVALID_FORM"
  | "INVALID_EMAIL"
  | "LOADING";

export async function getVerificationEmail(
  _prevValue: GetVerificationEmailResponse | undefined,
  formData: FormData,
): Promise<GetVerificationEmailResponse> {
  // get the email
  const email = formData.get("email");
  if (email == null) {
    console.log("Email not present");
    return "INVALID_FORM";
  }

  // request body
  const body = {
    email: email,
  };
  try {
    console.log("Body: " + JSON.stringify(body));

    // make the request
    const res = await fetchAPI("user/registration/initiate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    // if bad status
    if (res.status != 200) {
      return "INVALID_EMAIL";
    }

    return "SUCCESS";

  } catch (e) {
    console.error("Fetch error:", e);
    return "NETWORK_ERROR";
  }
}

export type CheckVerificationCodeResponse =
  | "SUCCESS"
  | "NETWORK_ERROR"
  | "INVALID_FORM"
  | "INVALID_CODE";

export async function checkVerificationCode(
  _prevValue: CheckVerificationCodeResponse | undefined,
  formData: FormData,
): Promise<CheckVerificationCodeResponse> {
  const email = formData.get("email");
  const code = formData.get("code");

  if (email == null || code == null) {
    return "INVALID_FORM";
  }

  const emailStr = encodeURIComponent(String(email));
  const codeStr = encodeURIComponent(String(code));

  try {
    console.log(
      "GET verify params:",
      JSON.stringify({ email: String(email), verification_token: String(code) }),
    );

    const res = await fetchAPI(
      `user/registration/code-verify?email=${emailStr}&verification_token=${codeStr}`,
      {
        method: "GET", //only GET was allowed
        headers: {
          "Content-Type": "application/json",
        },
  
      },
    );

    console.log("Fetched");
    console.log("Status:", res.status);
    console.log("Allow:", res.headers.get("allow"));

    if (res.status !== 200) {
      console.log("Bad request:", res.status);
      const text = await res.text();
      console.log("Response body:", text);
      return "INVALID_CODE";
    }

    const resBody = await res.json();
    console.log(resBody);

    return "SUCCESS";
  } catch (e) {
    console.log("Exception thrown");
    console.log(e);
    return "NETWORK_ERROR";
  }
}
export type RegistrationResponse =
  | "SUCCESS"
  | "INVALID_FORM"
  | "NETWORK_ERROR"
  | "PASSWORDS_DONT_MATCH"
  | "INVALID_REQUEST";
export async function completeRegistration(
  _prevValue: RegistrationResponse | undefined,
  formData: FormData,
): Promise<RegistrationResponse> {
  const email = formData.get("email");
  const code = formData.get("code");
  const password = formData.get("password");
  const passwordConfim = formData.get("password-confim");
  const firstName = formData.get("firstName");
  const lastName = formData.get("lastName");

  if (
    email == null ||
    code == null ||
    password == null ||
    passwordConfim == null
  ) {
    return "INVALID_FORM";
  }

  if (password != passwordConfim) {
    return "PASSWORDS_DONT_MATCH";
  }
  const body = {
    email: email,
    first_name: firstName,
    last_name: lastName,
    verification_token: code,
    password: password,
  };
  try {
    console.log("Body: " + JSON.stringify(body));

    let res = await fetchAPI("user/registration/verify", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    console.log("Fetched");
    if (res.status != 200) {
      return "INVALID_REQUEST";
    }

    const resBody = await res.json();

    console.log(resBody);

    return "SUCCESS";
  } catch (e) {
    console.log("Exception thrown");
    console.log(e);
    return "NETWORK_ERROR";
  }
}
