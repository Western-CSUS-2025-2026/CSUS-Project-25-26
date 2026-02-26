"use server";

import { cookies } from "next/headers";

export async function fetchAPIAuthorized(
  path: string,
  options: RequestInit,
): Promise<{ success: false } | { success: true; body: any }> {
  const url = process.env.API_URL;

  const user_cookies = await cookies();

  const token = user_cookies.get("session_token");

  if (url == undefined) {
    throw Error("ENV is not defined, API_URL must be defined as the api url");
  }

  const headers = new Headers(options.headers);
  if (token?.value) {
    headers.set("Authorization", `${token.value}`);
  }

  const res = await fetch(url + path, {
    ...options,
    headers,
  });

  if (!res.ok) {
    console.log("Bad Auth Request");
    console.log(res);
    console.log(await res.json());
    return { success: false };
  }
  const body = await res.json();
  console.log(body);
  return { success: true, body: body };
}
