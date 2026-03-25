import { fetchAPIAuthorized } from "../fetchAuth";

export async function createSession(templateId: number): Promise<
  | {
      success: false;
    }
  | { success: true; sessionId: string }
> {
  const res = await fetchAPIAuthorized("sessions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ template_id: templateId }),
  });

  if (!res.success) {
    console.log("Errors creating session");
    console.log(res);
    console.log("End ");

    return { success: false };
  }

  const body: { session_id: string } = res.body;

  return { success: true, sessionId: body.session_id };
}
