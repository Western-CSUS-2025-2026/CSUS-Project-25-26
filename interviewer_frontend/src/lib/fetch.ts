import { cookies } from "next/headers";

export function fetchAPI(
  path: string,
  options: { method?: string; headers?: Record<string, string>; body?: string },
) {
  const url = process.env.API_URL;
  if (url == undefined) {
    throw Error("ENV is not defined, API_URL must be defined as the api url");
  }
  const fullUrl = url + path;
  return fetch(fullUrl, options);
}
export async function fetchAPIAuthorized(
  path: string,
  options: { method: string; headers: Record<string, string>; body: string },
) {
  "use server";
  const url = process.env.API_URL;

  const user_cookies = await cookies();

  const token = user_cookies.get("session_token");

  if (token == undefined) {
    return;
  }

  if (url == undefined) {
    throw Error("ENV is not defined, API_URL must be defined as the api url");
  }

  const fullUrl = url + path;

  return await fetch(fullUrl, options);
}
