"use server";

import { fetchAPI } from "@/lib/fetch";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
export type LoginResponse =
  | "NOT_AUTHORIZED"
  | "SUCCESS"
  | "NETWORK_ERROR"
  | "UNVALID_FORM"
  | "LOADING";

export async function login(
  _prev: LoginResponse,
  formData: FormData,
): Promise<LoginResponse> {
  "use server";
  const email = formData.get("email");
  const password = formData.get("password");
  if (email == null || password == null || email == "" || password == "") {
    console.log("Email andd Password are required");
    return "UNVALID_FORM";
  }

  const userToken = await authenticateUser(
    email.toString(),
    password.toString(),
  );
  if (userToken == undefined) {
    return "NOT_AUTHORIZED";
  }

  const cookiesResolved = await cookies();
  cookiesResolved.set("session_token", userToken, {
    httpOnly: true,
    secure: true,
    maxAge: 60 * 60 * 24 * 7, // 1 week
  });

  redirect("/sessions");
}

async function authenticateUser(
  email: string,
  password: string,
): Promise<string | undefined> {
  const body = JSON.stringify({ email: email, password: password });

  const res = await fetchAPI("user/login", {
    headers: { "content-type": "application/json" },
    method: "POST",
    body: body,
  });

  console.log(res);
  if (!res.ok) {
    return undefined;
  }

  const responseBody: { token: string } = await res.json();

  return responseBody.token;
}
