import { cookies } from "next/headers";
export type LoginResponse =
  | "NOT_AUTHORIZED"
  | "SUCCESS"
  | "NETWORK_ERROR"
  | "UNVALID_FORM";

export async function login(formData: FormData): Promise<LoginResponse> {
  "use server";
  const email = formData.get("email");
  const password = formData.get("password");
  if (email == null || password == null) {
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
  cookiesResolved.set("sessionToken", userToken, {
    httpOnly: true,
    secure: true,
    maxAge: 60 * 60 * 24 * 7, // 1 week
  });
  return "SUCCESS";
}

async function authenticateUser(
  email: string,
  password: string,
): Promise<string | undefined> {
  return undefined;
}
