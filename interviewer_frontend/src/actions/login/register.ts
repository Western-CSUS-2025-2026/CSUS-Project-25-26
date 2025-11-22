export type GetVerificationEmailResponse =
  | "SUCCESS"
  | "NETWORK_ERROR"
  | "UNVALID_FORM";

export async function getVerificationEmail(
  formData: FormData,
): Promise<GetVerificationEmailResponse> {
  const email = formData.get("email");
  if (email == null) {
    return "UNVALID_FORM";
  }

  // make the request to send the code

  return "SUCCESS";
}

export type CheckVerificationCodeResponse =
  | "SUCCESS"
  | "NETWORK_ERROR"
  | "UNVALID_FORM"
  | "INVALID_CODE";

export async function checkVerificationCode(
  formData: FormData,
): Promise<CheckVerificationCodeResponse> {
  const email = formData.get("email");
  const code = formData.get("code");

  if (email == null || code == null) {
    return "UNVALID_FORM";
  }

  // make the request

  return "SUCCESS";
}
